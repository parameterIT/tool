from pathlib import Path
import subprocess
import sys
import importlib.util
import os
import csv
from datetime import date
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


def load_quality_model_from_args() -> QualityModel:
    if not Path(MODELS_PATH).exists():
        print(f"Make sure the models folder exists")
        exit(1)

    quality_model_name = sys.argv[2]
    spec = importlib.util.spec_from_file_location(
        "code_climate", MODELS_PATH + "/" + quality_model_name + ".py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["code_climate"] = module
    spec.loader.exec_module(module)
    # assumes that the python module has a variable model, that is an instantiation of the model class
    return module.model


def save_to_csv(quality_model, out="./output"):
    file_location = out + "/" + str(date.today()) + ".csv"
    if not os.path.exists(out):
        os.mkdir(out)
    with open(file_location, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        for metric, path in quality_model.getDesc()["metrics"].items():
            cmd = [f"./{path}", f"{src_root}"]
            process = subprocess.run(cmd, stdout=subprocess.PIPE)
            result = process.stdout.decode("utf-8").strip()
            writer.writerow([metric, result])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"Make sure to provide the path to source code and a name of a quality model to use currently have {sys.argv}"
        )
        exit(1)

    src_root: Path = parse_src_root()
    qm = load_quality_model_from_args()
    save_to_csv(qm)
    qm.set_results(Path("./output/2023-02-24.csv"))
    for name, aggregation in qm.getDesc()["aggregations"].items():
        print(name, aggregation())
    dashboard = Dashboard()
    dashboard.show_graphs()
