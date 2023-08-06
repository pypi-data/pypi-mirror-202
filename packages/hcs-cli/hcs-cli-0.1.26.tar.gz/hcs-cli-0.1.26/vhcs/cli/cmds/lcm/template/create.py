import sys
import click
from vhcs.service import lcm
from vhcs.common.ctxp.util import option_id_only


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
@option_id_only
def create(file: str, type: str, id_only: bool):
    """Create a template"""

    with file:
        payload = file.read()
    ret = lcm.template.create(payload, type)

    if id_only:
        return ret.get("id")
    return ret
