from urllib.request import urlopen
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
    r = urlopen(
        "https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py"
    )
    env = os.environ.copy()
    home = os.path.expanduser("~")
    poetry_wrapper = f"{home}/.local/share/poetry-wrapper"
    poetry_home = f"{poetry_wrapper}/{version}"
    env["POETRY_HOME"] = poetry_home
    os.makedirs(f"{poetry_wrapper}/{version}", exist_ok=True)
    p = subprocess.Popen(
        ["python", "-", "--version", version] + sys.argv[1:],
        stdin=subprocess.PIPE,
        env=env,
    )
    p.communicate(r.read())
    with open(f"{poetry_wrapper}/poetry.env", "w") as f:
        f.write(
            textwrap.dedent(
                """\
                poetry ()
                {
                    if [ -z "${POETRY_HOME}" ]; then
                        echo "POETRY_HOME not set";
                        return;
                    fi;
                    if [ "$1" == "shell" ]; then
                        VIRTUAL_ENV="$(${POETRY_HOME}/bin/poetry env info -p)";
                        if [ -f "$VIRTUAL_ENV/bin/activate" ] ; then
                            . "$VIRTUAL_ENV/bin/activate";
                        else
                            echo "No virtualenv found, run poetry install";
                        fi
                    else
                        ${POETRY_HOME}/bin/poetry "${@}";
                    fi
                }
                """
            )
        )

    os.makedirs(f"{home}/.bashrc.d", exist_ok=True)
    with open(f"{home}/.bashrc.d/poetry.env", "w") as f:
        f.write(
            textwrap.dedent(
                f"""\
                export POETRY_HOME="{poetry_home}"
                . {poetry_wrapper}/poetry.env
                """
            )
        )


if __name__ == "__main__":
    sys.exit(main())
