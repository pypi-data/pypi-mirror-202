#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
from argparse import ArgumentParser

from brainframe.api import BrainFrameAPI, bf_errors
from brainframe_apps.logger_factory import log

from brainframe_apps.command_utils import command, subcommand_parse_args, by_name


def set_license(api, license_file, no_print=True):
    with open(license_file, "r") as fp:
        license_key = fp.readlines()

    try:
        license_info = api.set_license_key(str(license_key))
        is_it_valid = license_info.state
        terms = license_info.terms
        message_str = f"License is {is_it_valid}\n {terms}"
    except Exception as e:
        message_str = f"Uploading license failed {e}: {license_key}"

    if no_print:
        log.debug(message_str)
    else:
        print(message_str)


def get_license(api, no_print=True):
    try:
        license_info = api.get_license_info()
        is_it_valid = license_info.state
        terms = license_info.terms
        message_str = f"License is {is_it_valid}\n {terms}"
    except Exception as e:
        message_str = f"Get license failed {e}"

    if no_print:
        log.debug(message_str)
    else:
        print(message_str)


def _license_control_parse_args(parser):
    parser.add_argument(
        "--server-url",
        default="http://localhost",
        help="The BrainFrame server " "URL, Default: %(default)s",
    )
    parser.add_argument(
        "--license-file",
        default=None,
        help="The name of the license file. Default: %(default)s",
    )


@command("license_control")
def license_control():
    parser = ArgumentParser(
        description="Set license key/Read license to/from a BrainFrame sever"
    )
    _license_control_parse_args(parser)
    args = subcommand_parse_args(parser)

    # Connect to BrainFrame server
    api = BrainFrameAPI(args.server_url)

    log.debug(f"{str(parser.prog)} Waiting for server at {args.server_url} ...")

    try:
        api.wait_for_server_initialization(timeout=15)
    except (TimeoutError, bf_errors.ServerNotReadyError):
        log.error(f"BrainFrame server connection timeout")
        return

    if args.license_file is not None:
        set_license(api, args.license_file)
    else:
        get_license(api)

    return


if __name__ == "__main__":
    by_name["license_control"]()
