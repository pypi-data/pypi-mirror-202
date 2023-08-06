from pathlib import Path
from datetime import datetime, timedelta

import click
from pygit2 import discover_repository, init_repository, Repository, Signature
from pygit2 import GIT_SORT_REVERSE, GIT_DIFF_REVERSE, GIT_DIFF_SHOW_BINARY, GIT_APPLY_LOCATION_BOTH
from git_timemachine.utils import print_error


@click.command('migrate')
@click.argument('src_dir', type=click.Path(exists=True, file_okay=False), default=Path.cwd())
@click.argument('dest_dir', type=click.Path(exists=False, file_okay=False), required=False, default=None)
@click.option('-o', '--offset', required=False, help='Time offset for each commit.')
@click.option('--default-head', help='Reference name of default HEAD', type=str, default='main')
@click.pass_context
def migrate_command(ctx: click.Context, src_dir: Path, dest_dir: Path, **options: dict):
    """Migrate commit logs from a repository to another."""

    src_dir = Path(src_dir)

    if dest_dir is None:
        dest_dir = src_dir.parent.joinpath(src_dir.name + '.migrated')

    if dest_dir.exists():
        raise FileExistsError(f'Destination directory {dest_dir} already exists.')

    dest_dir.mkdir(0o755)

    src_repo = Repository(discover_repository(src_dir))
    dest_repo = init_repository(dest_dir, initial_head='main')

    parent = []

    ref_name = f'refs/heads/{options["default_head"]}'

    for commit in src_repo.walk(src_repo.head.target, GIT_SORT_REVERSE):
        if len(commit.parents) > 0:
            diff = commit.tree.diff_to_tree(commit.parents[0].tree, flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)
        else:
            diff = commit.tree.diff_to_tree(flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)

        dest_repo.apply(diff, location=GIT_APPLY_LOCATION_BOTH)
        dest_repo.index.write()

        tree = dest_repo.index.write_tree()

        if tree is None:
            print_error('Failed to write index tree.')
            ctx.exit(1)

        seconds = 0
        if options['offset'] is not None:
            unit = options['offset'][-1]
            multi = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}

            if unit not in multi:
                raise ValueError(f'Unknown offset unit: {unit}')

            seconds = int(options['offset'][:-1]) * multi[unit]

        dt = datetime.fromtimestamp(commit.author.time) + timedelta(seconds=seconds)

        author = Signature(
            name=commit.author.name,
            email=commit.author.email,
            time=int(dt.timestamp()),
            encoding='utf-8',
            offset=int(dt.astimezone().tzinfo.utcoffset(dt).seconds / 60)
        )

        committer = author

        oid = dest_repo.create_commit(ref_name, author, committer, commit.message, tree, parent)

        if oid is None:
            print_error('Failed to create commit.')
            ctx.exit(1)

        parent = [dest_repo.head.target]
