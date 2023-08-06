from pathlib import Path
from typing import Union

import click
from git_timemachine.commands import command_group
from git_timemachine.state import StateFile


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
@click.option('--state-file', help='Path of state file.', type=click.Path(dir_okay=False, exists=False), is_eager=True, default=Path.home().joinpath('.git-timemachine.state'))
@click.pass_context
def cli(ctx: click.Context, state_file: Union[Path, str]):
    """A nested command-line utility that helps you record commits on Git repositories at any time node."""

    ctx.ensure_object(dict)
    ctx.obj['states'] = StateFile(Path(state_file))


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli()
