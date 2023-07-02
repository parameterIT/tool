import subprocess


def run():
    subprocess.run(
        ["poetry", "run", "python", "-u", "-m", "unittest", "discover", "-s", "core"]
    )
    subprocess.run(
        [
            "poetry",
            "run",
            "python",
            "-u",
            "-m",
            "unittest",
            "discover",
            "-s",
            "metrics/test",
        ]
    )
