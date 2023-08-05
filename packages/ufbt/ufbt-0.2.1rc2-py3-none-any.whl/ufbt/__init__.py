#
# CLI script entry point for uFBT
# This file is part of uFBT <https://github.com/flipperdevices/flipperzero-ufbt>
# Copyright (C) 2022-2023 Flipper Devices Inc.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import pathlib
import platform
import sys

from .bootstrap import bootstrap_cli, bootstrap_subcommands, get_ufbt_package_version

__version__ = get_ufbt_package_version()


def ufbt_cli():
    if not os.environ.get("UFBT_STATE_DIR"):
        os.environ["UFBT_STATE_DIR"] = os.path.expanduser("~/.ufbt")
    if not os.environ.get("FBT_TOOLCHAIN_PATH"):
        os.environ["FBT_TOOLCHAIN_PATH"] = os.environ["UFBT_STATE_DIR"]

    ufbt_state_dir = pathlib.Path(os.environ["UFBT_STATE_DIR"])

    # if any of bootstrap subcommands are in the arguments - call it instead
    # kept for compatibility with old scripts, better use `ufbt-bootstrap` directly
    if any(map(sys.argv.__contains__, bootstrap_subcommands)):
        return bootstrap_cli()

    if not os.path.exists(ufbt_state_dir):
        bootstrap_cli()

    if not (ufbt_state_dir / "current" / "scripts" / "ufbt").exists():
        print("SDK is missing scripts distribution!")
        print("You might be trying to use an SDK in an outdated format.")
        print("Run `ufbt update -h` for more information on how to update.")
        return 1

    UFBT_APP_DIR = os.getcwd()

    if platform.system() == "Windows":
        commandline = (
            'call "%UFBT_STATE_DIR%/current/scripts/toolchain/fbtenv.cmd" env & '
            f'python -m SCons -Q --warn=target-not-built -C "%UFBT_STATE_DIR%/current/scripts/ufbt" "UFBT_APP_DIR={UFBT_APP_DIR}" '
            + " ".join(sys.argv[1:])
        )

    else:
        commandline = (
            '. "$UFBT_STATE_DIR/current/scripts/toolchain/fbtenv.sh" && '
            f'python3 -m SCons -Q --warn=target-not-built -C "$UFBT_STATE_DIR/current/scripts/ufbt" "UFBT_APP_DIR={UFBT_APP_DIR}" '
            + " ".join(sys.argv[1:])
        )

    # print(commandline)
    return os.system(commandline)


if __name__ == "__main__":
    sys.exit(ufbt_cli() or 0)
