import pandas as pd
import logging
import time
import csv

from typing import Dict
from pathlib import Path

from core.metric.result import Result


class Writer:
    def write_to_csv(self, results: Dict, output_dir, model_name, path):
        """
        write_to_csv generates a csv file containing aggregation results and
        underlying metrics

        _write_to_csv will for each dictionary entry write either the associated
        outcome when running a metric, or the aggregation result to a csv
        file and output it in the outcomes folder

        the naming naming format is YYYY-MM-DD_HH-MM-SS so that dashboard.py can
        use it to display data chronologically
        """
        # See https://docs.python.org/3/library/time.html#time.strftime for table
        # explaining formattng
        # Format: YYYY-MM-DD_HH-MM-SS
        logging.info("Writing to csv")

        current_time: str = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        file_name = Path(current_time + ".csv")
        try:
            self._save_meta_data(output_dir, model_name, path, file_name)
            self._save_outcomes(results, output_dir, file_name)
            self._save_violations(results, output_dir, file_name)
        except Exception as ex:
            logging.error(f"failed to save to csv. Exception: {ex}")
            raise RuntimeError

        logging.info("Finished writing to csv")

    def _save_meta_data(self, output_dir, model_name, path, file_name):
        """
        _save_meta_data will save the relevant metadata such as thea
        quality model used and the src path
        """
        file_location = output_dir / Path("metadata") / file_name
        with open(file_location, "w") as metadata_file:
            writer = csv.writer(metadata_file)
            writer.writerow([f"qualitymodel", "src_root"])
            writer.writerow([model_name, path.__str__()])
        logging.info("Finished writing metadata to csv")

    def _save_outcomes(self, results, output_dir, file_name):
        """
        _save_outcome will save the outcome mapping for the amount of
        violations of each metric
        """
        file_location = output_dir / Path("outcomes") / file_name
        with open(file_location, "w") as results_file:
            writer = csv.writer(results_file)
            writer.writerow(["metric", "value"])
            for description, value in results.items():
                outcome = value
                if type(value) is Result:
                    outcome = value.outcome
                writer.writerow([description, outcome])
        logging.info("Finished writing outcomes to csv")

    def _save_violations(self, results: Dict, output_dir, file_name):
        """
        _generate_violations_table generates a csv file in the output/violations/ folder containing
        the locations of all found violations during parsing of the code base

        _generate_violations_table given a dictionary of metrics will generate a csv file using
        pandas. Because the dictionary may contain aggregation results that isn't of type Result,
        and therefore doesn't contain locations of violations, we continue upon meeting an element
        not of type Result.
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
        file_location = Path(output_dir / Path("violations") / file_name)
        violations.to_csv(file_location)

    def gen_output_paths_if_not_exists(self, output_dir):
        """
        gen_output_paths_if_not_exists will generate the output paths
        needed before saving the files
        """
        Path(output_dir).resolve().mkdir(parents=True, exist_ok=True)
        Path(output_dir / Path("violations")).resolve().mkdir(
            parents=True, exist_ok=True
        )
        Path(output_dir / Path("outcomes")).resolve().mkdir(parents=True, exist_ok=True)
        Path(output_dir / Path("metadata")).resolve().mkdir(parents=True, exist_ok=True)
