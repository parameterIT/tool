from pathlib import Path
import subprocess
import sys
import os
import csv
from datetime import date
from byoqm.models.code_climate import CodeClimate
from byoqm.visuals.dashboard import Dashboard
from byoqm.qualitymodel.qualitymodel import QualityModel
from visuals import line


def parse_src_root() -> Path:
    if len(sys.argv) == 1:
        print("Make sure to provide the path to source code")
        exit(1)

    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


def save_to_csv(quality_model, out="./output"):
    file_location = out + "/" + str(date.today()) + ".csv"
    if not os.path.exists(out):
        os.mkdir(out)
    with open(file_location, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])
        for metric, path in quality_model.getDesc()["metrics"].items():
            cmd = [f"./{path}", f"{src_root}"]
            process = subprocess.run(cmd, stdout=subprocess.PIPE)
            result = process.stdout.decode("utf-8").strip()
            writer.writerow([metric, result])


if __name__ == "__main__":
    src_root: Path = parse_src_root()
    qm: QualityModel = CodeClimate()
    save_to_csv(qm)
    qm.set_results(Path("./output/2023-02-24.csv"))
    for name, aggregation in qm.getDesc()["aggregations"].items():
        print(name, aggregation())
    dashboard = Dashboard()
    dashboard.show_graphs()
