import os
import random
from pathlib import Path
from datetime import datetime, timedelta

import click
from tabulate import tabulate
from pygit2 import discover_repository, Repository, Signature, GitError
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_RENAMED, GIT_STATUS_INDEX_MODIFIED
from pygit2 import GIT_STATUS_INDEX_DELETED, GIT_STATUS_INDEX_TYPECHANGE, GIT_STATUS_WT_NEW
from git_timemachine.state import StateFile
from git_timemachine.utils import print_error


def status_text(status: int) -> str:
    texts = {
        GIT_STATUS_INDEX_NEW: 'new',
        GIT_STATUS_INDEX_MODIFIED: 'modified',
        GIT_STATUS_INDEX_DELETED: 'deleted',
        GIT_STATUS_INDEX_RENAMED: 'renamed',
        GIT_STATUS_INDEX_TYPECHANGE: 'type changed'
    }

    result = []
    for i, text in texts.items():
        if status & i == i:
            result.append(text)

    return ', '.join(result)


@click.command('commit')
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=Path.cwd())
@click.option('-m', '--message', help='Message describing the changes.', required=True)
@click.option('--rand-min', help='Minimum random seconds of time increase.', type=int, default=600)
@click.option('--rand-max', help='Maximum random seconds of time increase.', type=int, default=3600)
@click.option('--default-head', help='Reference name of default HEAD', type=str, default='main')
@click.pass_context
def commit_command(ctx: click.Context, repo_dir: str, **options: dict):
    """Record a commit on repository based on time states."""

    states: StateFile = ctx.obj['states']
    last_commit = states.get('last-commit')

    if last_commit is None:
        print_error('state "last-commit" not defined, current time used.')
        states.set('last-commit', datetime.now())
        states.save()
        ctx.exit()

    repo = Repository(discover_repository(repo_dir))
    pre_commit = Path(repo.path, 'hooks', 'pre-commit')
    if pre_commit.exists():
        assert os.system(pre_commit) == 0

    repo_status = repo.status(untracked_files='no')

    if repo_status == {} or len([value for value in repo_status.values() if value < GIT_STATUS_WT_NEW]) < 1:
        raise GitError(f'Nothing to commit on "{repo_dir}".')

    random.seed()
    dt = last_commit + timedelta(seconds=random.randint(options['rand_min'], options['rand_max']))

    if not repo.head_is_unborn and dt.timestamp() < next(repo.walk(repo.head.target)).commit_time:
        raise GitError('HEAD time is later than commit time.')

    author = Signature(
        name=repo.default_signature.name,
        email=repo.default_signature.email,
        time=int(dt.replace(microsecond=0).timestamp()),
        encoding='utf-8',
        offset=int(dt.tzinfo.utcoffset(dt).seconds / 60)

    )

    committer = author

    parent = []

    if repo.head_is_unborn:
        ref_name = f'refs/heads/{options["default_head"]}'
    else:
        parent.append(repo.head.target)
        ref_name = repo.head.name

    tree = repo.index.write_tree()

    if tree is None:
        print_error('Failed to write index tree.')
        ctx.exit(1)

    oid = repo.create_commit(ref_name, author, committer, options['message'], tree, parent)

    if oid is None:
        print_error('Failed to create commit.')
        ctx.exit(1)

    table = []
    for file in repo_status:
        if repo_status[file] >= GIT_STATUS_WT_NEW:
            continue

        table.append([status_text(repo_status[file]), file])

    print(f'commit: {oid.hex}')
    print(f'committer: {committer.name} <{committer.email}>')
    print(f'datetime: {datetime.fromtimestamp(committer.time).astimezone().isoformat()}')
    print(f'message: {options["message"]}')
    print()
    print(tabulate(table, headers=['status', 'file']))

    states.set('last-commit', dt)
    states.save()
