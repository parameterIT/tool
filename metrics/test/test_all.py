import subprocess
import os


def run():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(
        ["python", "-u", "-m", "unittest"],
    )
    os.chdir("./metrics/test")
    subprocess.run(
        ["python", "-u", "-m", "unittest"],
    )
