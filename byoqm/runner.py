import subprocess
import time
import csv
import sys

import importlib.util
import importlib.machinery

from pathlib import Path
from typing import Dict

from test.test_support import os

from byoqm.qualitymodel.qualitymodel import QualityModel

# Assumes the project is being run from the root of the repository
_OUTPUT_DIR = Path("./output")
_MODELS_DIR = "models"


class Runner:
    def __init__(self, model_name: str, src_root: str):
        self._src_root: str = src_root
        self._model: QualityModel = self._load(model_name)
        self._model_name: str = model_name

    def _load(self, model_name: str) -> QualityModel:
        """
        Searches _MODELS_DIR for a python file named `name` to use as the model.
        """
        try:
            path_to_model = self._find_model_file(model_name)
            spec = importlib.util.spec_from_file_location("model", path_to_model)
            module = importlib.util.module_from_spec(spec)
            sys.modules["model"] = module
            spec.loader.exec_module(module)
            # Assumes any module describing a quality model has a top level mode
            # variable
            return module.model
        except FileNotFoundError:
            print(f"Failed to locate {model_name} in {_MODELS_DIR}")
            exit(1)

    def _find_model_file(self, model_name):
        path_to_model = _MODELS_DIR + "/" + model_name + ".py"
        if not os.path.exists(path_to_model):
            raise FileNotFoundError

        return path_to_model

    def run(self) -> Path:
        """
        Returns a path to a .csv file that contains the metric and aggregation results
        as defined by the currently loaded model.
        """
        results = self._run_aggregations()
        output = self._write_to_csv(results)
        return output

    def _run_aggregations(self) -> Dict:
        """
        Runs all the aggergations defined by the quality model.
        The `results` dictionary is updated as each aggregation is run, meaning that
        aggregations relying on other aggregations should be defined after its
        dependencies in the dictionary returned by a model's getDesc()
        """
        results = self._run_metrics()

        aggregations = self._model.getDesc()["aggregations"]
        for aggregation, aggregation_function in aggregations.items():
            results[aggregation] = aggregation_function(results)

        return results

    def _run_metrics(self) -> Dict:
        results = {}

        metrics = self._model.getDesc()["metrics"]
        for metric, exec_path in metrics.items():
            cmd = [f"./{exec_path}", f"{self._src_root}"]
            process = subprocess.run(cmd, stdout=subprocess.PIPE)
            result = process.stdout.decode("utf-8").strip()
            results[metric] = int(result)

        return results

    def _write_to_csv(self, results: Dict):
        # See https://docs.python.org/3/library/time.html#time.strftime for table
        # explaining formattng
        # Format: YYYY-MM-DD_HH-MM-SS
        current_time: str = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        file_name = Path(current_time + ".csv")
        file_location = _OUTPUT_DIR / file_name

        with open(file_location, "w") as results_file:
            writer = csv.writer(results_file)
            writer.writerow([f"qualitymodel={self._model_name}"])
            writer.writerow(["Metric", "Value"])
            for description, value in results.items():
                writer.writerow([description, value])

        return file_location
