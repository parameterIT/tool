from pathlib import Path
import sys
import importlib.util
from byoqm.visuals.dashboard import Dashboard
from byoqm.qualitymodel.qualitymodel import QualityModel
from visuals import line

# Assumes the project is being run from the root of the repository
MODELS_PATH = "models"


def parse_src_root() -> Path:
    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


def parse_quality_model() -> QualityModel:
    if not Path(MODELS_PATH).exists():
        print(f"Make sure the models folder exists")
        exit(1)

    quality_model_name = sys.argv[2]
    spec = importlib.util.spec_from_file_location(
        "code_climate", "models/code_climate.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["code_climate"] = module
    spec.loader.exec_module(module)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Make sure to provide the path to source code and a name of a quality model to use"
        )
        exit(1)

    parse_quality_model()
    src_root: Path = parse_src_root()

    # qm: QualityModel = CodeClimate()
    # qm.set_src_root(src_root)
    # print(qm.getDesc()["lines of code"]())
    # print(qm.getDesc()["return statements"]())
    # qm.getDesc()["identical blocks of code"](35)
    # qm.save_to_csv()
    # dashboard = Dashboard()
    # dashboard.show_graphs()
