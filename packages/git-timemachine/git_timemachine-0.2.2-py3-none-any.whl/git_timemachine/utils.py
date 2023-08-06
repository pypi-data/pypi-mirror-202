import click


def print_error(msg: str):
    click.echo(click.style(f'Error: {msg}', fg='red'), err=True)


def print_warning(msg: str):
    click.echo(click.style(f'Warning: {msg}', fg='yellow'))


def print_success(msg: str):
    click.echo(click.style(f'Success: {msg}', fg='green'))


def print_debug(msg: str):
    click.echo(click.style(f'Debug: {msg}', fg='cyan'))
