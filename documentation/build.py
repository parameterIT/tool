import subprocess
import os


def run():
    """
    Run all unittests. Equivalent to:
    `poetry run mkdocs build -c`
    `poetry run mkdocs serve`
    """
    os.chdir("./documentation")
    subprocess.run(
        ["mkdocs", "build", "-c"],
    )

    subprocess.run(
        ["mkdocs", "serve"],
    )
