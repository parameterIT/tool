import subprocess
import os


def run():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest`
    """
    os.chdir("./documentation")
    subprocess.run(
        ["mkdocs", "build", "-c"],
    )

    subprocess.run(
        ["mkdocs", "serve"],
    )
