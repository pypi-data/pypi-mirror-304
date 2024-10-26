import typer

import uv_audit
from uv_audit.manager import UvAuditManager

cli = typer.Typer(help='uv-audit CLI')


uv_audit_manager = UvAuditManager()


def version_callback(value: bool):
    if value:
        print(f'Version of uv-audit is {uv_audit.__version__}')
        raise typer.Exit(0)


@cli.command()
def command(  # noqa: C901
    ctx: typer.Context,
    #
    version: bool = typer.Option(
        False,
        '--version',
        callback=version_callback,
        help='Print version of uv-audit.',
        is_eager=True,
    ),
    # Setters
    extra: bool = typer.Option(
        True,
        '--extra',
        help='TODO',
        metavar='Default',
        rich_help_panel='uv-audit Options',
    ),
    dev: bool = typer.Option(
        True,
        '--dev',
        help='TODO',
        metavar='Default',
        rich_help_panel='uv-audit Options',
    ),
):
    errors = uv_audit_manager.scan()

    if errors > 1:
        raise typer.Exit(1)

    raise typer.Exit(0)
