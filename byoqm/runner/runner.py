import logging
import subprocess
import time
import csv
import sys
import pandas as pd

import importlib.util
import importlib.machinery

from pathlib import Path
from typing import Dict, List

from test.test_support import os
from byoqm.metric.metric import Metric
from byoqm.metric.result import Result

from byoqm.qualitymodel.qualitymodel import QualityModel
from byoqm.source_repository.source_repository import SourceRepository


class Runner:
    _MODELS_DIR = "models"

    def __init__(
        self,
        model_name: str,
        src_root: Path,
        output_path: Path,
        save_file: bool,
        language: str,
    ):
        self._shortenPath = src_root
        self._src_root: Path = src_root.resolve()
        self._model: QualityModel = self._load(model_name)
        self._model_name: str = model_name
        self._output_dir = output_path
        self._save_file = save_file
        self._source_repository = SourceRepository(self._src_root, language)

    def _load(self, model_name: str) -> QualityModel:
        """
        Searches _MODELS_DIR for a python file named `name` to use as the model.
        """
        path_to_model = self._find_model_file(model_name)
        spec = importlib.util.spec_from_file_location("model", path_to_model)
        module = importlib.util.module_from_spec(spec)
        sys.modules["model"] = module
        spec.loader.exec_module(module)
        # Assumes any module describing a quality model has a top level mode
        # variable
        return module.model

    def _find_model_file(self, model_name):
        path_to_model = self._MODELS_DIR + "/" + model_name + ".py"
        if not os.path.exists(path_to_model):
            logging.error(
                f"Path to model file doesnt exist. Path given: {path_to_model}"
            )
            raise FileNotFoundError
        return path_to_model

    def run(self) -> Path:
        """
        Returns a path to a .csv file that contains the metric and aggregation results
        as defined by the currently loaded model.
        """
        results = self._run_aggregations()
        if self._save_file:
            self._gen_output_paths_if_not_exists()
            output = self._write_to_csv(results)
            return output
        return None

    def _run_aggregations(self) -> Dict:
        """
        Runs all the aggergations defined by the quality model.
        The `results` dictionary is updated as each aggregation is run, meaning that
        aggregations relying on other aggregations should be defined after its
        dependencies in the dictionary returned by a model's getDesc()
        """
        results = self._run_metrics()
        logging.info("Started running aggregations")
        aggregations = self._model.getDesc()["aggregations"]
        for aggregation, aggregation_function in aggregations.items():
            results[aggregation] = aggregation_function(results)
        logging.info("Finished running aggregations")
        return results

    def _run_metrics(self) -> Dict:
        """
        runs all associated metric files specified in the models description
        by creating instances of metrics and calling their run() method, fi-
        nally returning a dictionary of metric results.
        """
        results = {}
        logging.info("Started running metrics")
        metrics = self._model.getDesc()["metrics"]
        for metric, metric_file in metrics.items():
            spec = importlib.util.spec_from_file_location("metric", metric_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[metric] = module
            spec.loader.exec_module(module)
            module.metric._source_repository = self._source_repository
            results[metric] = module.metric.run()
        logging.info("Finished running metrics")
        return results

    def _generate_violations_table(self, results: Dict, time: str):
        """
        _generate_violations_table generates a csv file in the output/violations/ folder containing
        the locations of all found violations during parsing of the code base

        _generate_violations_table generates given a dictionary of metrics, constructs a list containing
        all locations from which a pandas dataframe is generated. Finally, the dataframe is written to a
        csv file using pandas, and output in the specified violations folder.
        """
        list_of_violations = []
        for _, result in results.items():
            if type(result) is not Result:
                continue
            for location in result.get_violation_locations():
                list_of_violations.extend([[result.metric, location]])
        violations = pd.DataFrame(
            list_of_violations, columns=["type", "file_start_end"]
        )
        file_location = Path(
            self._output_dir / Path("violations") / Path(time + ".csv")
        )
        violations.to_csv(file_location)

    def _write_to_csv(self, results: Dict):
        """
        _write_to_csv generates a csv file containing aggregation results and
        underlying metrics

        _write_to_csv will for each dictionary entry write either the associated
        frequency of violations for a metric, or the aggregation result to a csv
        file and output it in the frequencies folder

        the naming naming format is YYYY-MM-DD_HH-MM-SS so that dashboard.py can
        use it to display data chronologically
        """
        # See https://docs.python.org/3/library/time.html#time.strftime for table
        # explaining formattng
        # Format: YYYY-MM-DD_HH-MM-SS
        logging.info("Writing to csv")
        current_time: str = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        file_name = Path(current_time + ".csv")

        self._generate_violations_table(results, current_time)

        file_location = self._output_dir / Path("frequencies") / file_name
        with open(file_location, "w") as results_file:
            writer = csv.writer(results_file)
            writer.writerow(["metric", "value"])
            for description, value in results.items():
                frequency = value
                if type(value) is Result:
                    frequency = value.get_frequency()
                writer.writerow([description, frequency])
        logging.info("Finished writing frequencies to csv")
        file_location = self._output_dir / Path("metadata") / file_name
        with open(file_location, "w") as metadata_file:
            writer = csv.writer(metadata_file)
            writer.writerow([f"qualitymodel", "src_root"])
            writer.writerow([self._model_name, self._shortenPath.__str__()])
        logging.info("Finished writing metadata to csv")
        return file_location

    def _gen_output_paths_if_not_exists(self):
        Path(self._output_dir / Path("violations")).resolve().mkdir(exist_ok=True)
        Path(self._output_dir / Path("frequencies")).resolve().mkdir(exist_ok=True)
        Path(self._output_dir / Path("metadata")).resolve().mkdir(exist_ok=True)
