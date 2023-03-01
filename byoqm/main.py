from pathlib import Path
import sys
from byoqm.runner import Runner
from byoqm.visuals.dashboard import Dashboard
from visuals import line

# Assumes the project is being run from the root of the repository
MODELS_PATH = "models"


def parse_src_root() -> Path:
    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"Make sure to provide the path to source code and a name of a quality model to use currently have {sys.argv}"
        )
        exit(1)

    runner: Runner = Runner("code_climate", "byoqm")
    runner.run()

    # dashboard = Dashboard()
    # dashboard.show_graphs()
