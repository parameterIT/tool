import logging
import sys


import importlib.util
import importlib.machinery

from pathlib import Path
from typing import Dict

import os

from core.qualitymodel.qualitymodel import QualityModel
from core.source_repository.source_repository import SourceRepository


class Runner:
    _MODELS_DIR = "models"

    def __init__(
        self,
        model_name: str,
        src_root: Path,
    ):
        self._model: QualityModel = self._load(model_name)
        self._source_repository = SourceRepository(src_root.resolve())

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

    def run(self) -> Dict:
        """
        Returns a path to a .csv file that contains the metric and aggregation results
        as defined by the currently loaded model.
        """
        try:
            return self._run_aggregations()
        except:
            logging.error("failed to run aggregations")
            raise RuntimeError

    def _run_aggregations(self) -> Dict:
        """
        Runs all the aggergations defined by the quality model.
        The `results` dictionary is updated as each aggregation is run, meaning that
        aggregations relying on other aggregations should be defined after its
        dependencies in the dictionary returned by a model's get_desc()
        """
        try:
            results = self._run_metrics()
            logging.info("Started running aggregations")
            aggregations = self._model.get_desc()["aggregations"]
            for aggregation, aggregation_function in aggregations.items():
                results[aggregation] = aggregation_function(results)
            logging.info("Finished running aggregations")
            return results
        except Exception as ex:
            logging.error(f"Failed to run metrics. Exception: {ex}")
            raise RuntimeError

    def _run_metrics(self) -> Dict:
        """
        runs all associated metric files specified in the models description
        by creating instances of metrics and calling their run() method, fi-
        nally returning a dictionary of metric results.
        """
        results = {}
        logging.info("Started running metrics")
        metrics = self._model.get_desc()["metrics"]
        for metric, metric_file in metrics.items():
            spec = importlib.util.spec_from_file_location("metric", metric_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[metric] = module
            spec.loader.exec_module(module)
            module.metric._source_repository = self._source_repository
            results[metric] = module.metric.run()
        logging.info("Finished running metrics")
        return results
