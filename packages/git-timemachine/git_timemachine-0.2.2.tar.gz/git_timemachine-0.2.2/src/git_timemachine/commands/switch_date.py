from datetime import timedelta

import click
from git_timemachine.state import StateFile


@click.command('switch-date')
@click.option('-d', '--days', help='Days to switch for last committed.', type=int, default=1)
@click.option('-h', '--begin-hour', help='Hour to begin with.', type=int, default=10)
@click.pass_context
def switch_date_command(ctx: click.Context, **options: dict):
    """Switch the date of last committed."""

    states: StateFile = ctx.obj['states']
    dt = states.get('last-commit') + timedelta(hours=options['days'] * 24)
    states.set('last-commit', dt.replace(hour=options['begin_hour'], minute=0, second=0, microsecond=0))
    states.save()
