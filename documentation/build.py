import subprocess
import os


def run():
    """
    Build and run docs. Equivalent to:
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
