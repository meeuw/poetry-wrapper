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
                        . "$(${POETRY_HOME}/bin/poetry env info -p)/bin/activate";
                    else
                        ${POETRY_HOME}/bin/poetry ${@};
                    fi
                }
                """
            )
        )
    update_profile(poetry_home, poetry_wrapper, home)


def update_profile(poetry_home, poetry_wrapper, home):
    addition = f'\nexport POETRY_HOME="{poetry_home}"\n. {poetry_wrapper}/poetry.env\n'

    with open(f"{home}/.bashrc") as f:
        content = f.read()

    updated, number_of_subs_made = re.subn(
        r'\nexport POETRY_HOME=".*"\n\. .*/poetry.env\n', addition, content, 1
    )

    if number_of_subs_made == 0:
        with open(f"{home}/.bashrc", "a") as f:
            f.write(addition)
    else:
        with open(f"{home}/.bashrc", "w") as f:
            f.write(updated)


if __name__ == "__main__":
    sys.exit(main())
