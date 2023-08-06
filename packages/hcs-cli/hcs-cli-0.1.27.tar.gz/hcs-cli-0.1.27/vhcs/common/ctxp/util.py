import json
import yaml
import sys
import click


class CtxpException(Exception):
    pass


def print_output(data: any, output: str = "json"):
    if type(data) is str:
        text = data
    elif output == "json":
        text = json.dumps(data, indent=4)
    elif output == "json-compact":
        text = json.dumps(data)
    elif output == "yaml":
        import vhcs.common.ctxp as ctxp
        text = yaml.dump(ctxp.jsondot.plain(data))
    elif output == "text":
        if isinstance(data, list):
            text = ""
            for i in data:
                line = i if type(i) is str else json.dumps(i)
                text += line + "\n"
        elif isinstance(data, dict):
            text = json.dumps(data, indent=4)
        else:
            text = json.dumps(data, indent=4)
    else:
        raise Exception(f"Unexpected output format: {output}")
    
    print(text, end="")


def panic(reason: any = None, code: int = 1):
    print(reason, file=sys.stderr)
    sys.exit(code)


option_verbose = click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="Print debug logs",
)

option_output = click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "json-compact", "yaml", "text"]),
    default="json",
    help="Specify output format",
)

option_id_only = click.option(
    "--id-only/--full-object",
    type=bool,
    default=False,
    required=False,
    help="Output only the object, instead of the full data object"
)
