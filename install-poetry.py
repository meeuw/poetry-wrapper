from urllib.request import urlopen, urlretrieve
import subprocess
import sys
import tempfile
import shutil
import os
import argparse
import textwrap
import re


def main():
    parser = argparse.ArgumentParser(
        description="Installs the latest (or given) version of poetry"
    )
    parser.add_argument(
        "--version", help="install named version", dest="version", required=True
    )
    args = parser.parse_args()

    version = args.version
    home = os.path.expanduser("~")
    poetry_wrapper = f"{home}/.local/share/poetry-wrapper"
    poetry_home = f"{poetry_wrapper}/{version}"

    r = urlopen(
        "https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py"
    )
    env = os.environ.copy()
    env["POETRY_HOME"] = poetry_home
    os.makedirs(f"{poetry_wrapper}/{version}", exist_ok=True)
    p = subprocess.Popen(
        ["python", "-", "--version", version] + sys.argv[1:],
        stdin=subprocess.PIPE,
        env=env,
    )
    p.communicate(r.read())

    os.makedirs(f"{home}/.bashrc.d", exist_ok=True)
    urlretrieve("https://raw.githubusercontent.com/meeuw/poetry-wrapper/master/poetry.env", f"{home}/.bashrc.d/poetry.env")

if __name__ == "__main__":
    sys.exit(main())
