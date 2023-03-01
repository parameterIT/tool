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
    if len(sys.argv) < 2:
        print(
            "Make sure to provide the path to source code and a name of a quality model to use"
        )
        exit(1)

    parse_quality_model()
    src_root: Path = parse_src_root()
    qm: QualityModel = CodeClimate()
    save_to_csv(qm)
    qm.set_results(Path("./output/2023-02-24.csv"))
    for name, aggregation in qm.getDesc()["aggregations"].items():
        print(name, aggregation())
    dashboard = Dashboard()
    dashboard.show_graphs()
