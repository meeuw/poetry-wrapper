import tempfile
import importlib
import sys
import os
import textwrap

sys.path.append(os.getcwd())
install_poetry = importlib.import_module("install-poetry")


def test_update_profile():
    with tempfile.TemporaryDirectory() as home:
        with open(f"{home}/.bashrc", "w") as f:
            f.write(
                textwrap.dedent(
                    """\
                    # .bashrc
                    """
                )
            )
        install_poetry.update_profile("path/to/poetry/home", "path/to/poetry_wrapper", home)
        with open(f"{home}/.bashrc") as f:
            assert f.read() == textwrap.dedent(
                """\
                    # .bashrc

                    export POETRY_HOME="path/to/poetry/home"
                    . path/to/poetry_wrapper/poetry.env
                """
            ), "update add"
        install_poetry.update_profile("path/to/poetry/home", "path/to/poetry_wrapper", home)
        with open(f"{home}/.bashrc") as f:
            assert f.read() == textwrap.dedent(
                """\
                    # .bashrc

                    export POETRY_HOME="path/to/poetry/home"
                    . path/to/poetry_wrapper/poetry.env
                """
            ), "update existing"
