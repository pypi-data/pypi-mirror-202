#!/usr/bin/env -S python3 -W ignore

import sys
import json
import httpx
import click
import os.path as path
import logging

_script_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), "."))
_module_dir = path.dirname(_script_dir)
if __name__ == "__main__":
    _cli_dir = path.dirname(_module_dir)
    sys.path.append(_cli_dir)

import vhcs.common.ctxp as ctxp
from vhcs.common.ctxp.util import option_output, option_verbose

# -----------------------------------------------------------
import vhcs.common.logger as logger

logger.setup()
logging.getLogger("charset_normalizer").setLevel(logging.WARN)
logging.getLogger("csp").setLevel(logging.INFO)
logging.getLogger("context").setLevel(logging.WARN)
logging.getLogger("init").setLevel(logging.WARN)
logging.getLogger("profile").setLevel(logging.WARN)
# -----------------------------------------------------------


@click.group()
@click.version_option(package_name="hcs-cli")
@option_verbose
@option_output
@click.option("--profile", "-p", type=str, required=False, help="Specify the profile to use. Optional.")
@click.option("--upgrade-check/--no-upgrade-check", default=True, help="Check new version of HCS CLI.")
@click.option("--telemetry/--no-telemetry", default=True, help="Send telemetry")
def cli(verbose: bool, output: str, profile: str, upgrade_check: bool, telemetry: bool):

    if upgrade_check:
        from vhcs.util.versions import check_upgrade

        check_upgrade()
    if profile:
        ctxp.profile._active_profile_name = profile


# @cli.result_callback()
# def _process_result(result, **kwargs):
#     print("_process_result", result, kwargs)
#     pass


def main():
    try:
        commands_dir = path.join(_module_dir, "cli/cmds")
        config_path = path.join(_module_dir, "config")
        ctxp.init(cli_name="hcs", main_cli=cli, commands_dir=commands_dir, config_path=config_path)
    except ctxp.CtxpException as e:
        ctxp.panic(e)
    except httpx.HTTPStatusError as e:
        import traceback
        traceback.print_exc()
        try:
            err = json.loads(e.response.text)
        except:
            err = {
                "message": str(e),
                "response": e.response.text,
                "resource": str(e.request.url)
            }
        text = json.dumps(err, indent=4)
        ctxp.panic(text)


if __name__ == "__main__":
    main()
