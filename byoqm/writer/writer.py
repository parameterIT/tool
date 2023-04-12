import pandas as pd
import logging
import time
import csv

from typing import Dict
from pathlib import Path

from byoqm.metric.result import Result


class Writer:
    def __init__(
        self,
        model_name,
        src_root,
        output_dir,
    ):
        self._model_name = model_name
        self._shortened_path = src_root
        self._output_dir = output_dir
        current_time: str = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        self._file_name = Path(current_time + ".csv")

    def run(self, results):
        """
        run ensures that the output path exists and thereafter starts saving the
        respective files
        """
        if results == None:
            logging.error("Results is none. Skipping writing...")
            return
        self._gen_output_paths_if_not_exists()
        self._write_to_csv(results)

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

        self._save_meta_data()
        self._save_frequencies(results)
        self._save_violations(results)
        logging.info("Finished writing to csv")

    def _save_meta_data(self):
        """
        _save_meta_data will save the relevant metadata such as the
        quality model used and the src path
        """
        file_location = self._output_dir / Path("metadata") / self._file_name
        with open(file_location, "w") as metadata_file:
            writer = csv.writer(metadata_file)
            writer.writerow([f"qualitymodel", "src_root"])
            writer.writerow([self._model_name, self._shortened_path.__str__()])
        logging.info("Finished writing metadata to csv")

    def _save_frequencies(self, results):
        """
        _save_frequencies will save the frequency mapping for the amount of
        violations of each metric
        """
        file_location = self._output_dir / Path("frequencies") / self._file_name
        with open(file_location, "w") as results_file:
            writer = csv.writer(results_file)
            writer.writerow(["metric", "value"])
            for description, value in results.items():
                frequency = value
                if type(value) is Result:
                    frequency = value.get_frequency()
                writer.writerow([description, frequency])
        logging.info("Finished writing frequencies to csv")

    def _save_violations(self, results: Dict):
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
        file_location = Path(self._output_dir / Path("violations") / self._file_name)
        violations.to_csv(file_location)

    def _gen_output_paths_if_not_exists(self):
        """
        _gen_output_paths_if_not_exists will generate the output paths
        needed before saving the files
        """
        Path(self._output_dir).resolve().mkdir(exist_ok=True)
        Path(self._output_dir / Path("violations")).resolve().mkdir(exist_ok=True)
        Path(self._output_dir / Path("frequencies")).resolve().mkdir(exist_ok=True)
        Path(self._output_dir / Path("metadata")).resolve().mkdir(exist_ok=True)
