import csv
import unittest

from pathlib import Path

from test.test_support import os, shutil
from byoqm.visuals import Dashboard
from datetime import datetime

_TEST_FOLDER = Path("./test")
_OUTPUT_FOLDER = _TEST_FOLDER / Path("test")
_METRIC_NAME = "file_length"


class TestDashboard(unittest.TestCase):
    def setUp(self):
        _OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        self._seed_files()

    def _seed_files(self):
        files = [
            Path("2023-03-02_13-57-34.csv"),
            Path("2023-03-02_23-59-59"),
            Path("2023-03-03_00-00-01.csv"),
            Path("2023-04-02_00-00-01.csv"),
            Path("2024-03-02_00-00-01.csv"),
        ]
        for file in files:
            filepath = _OUTPUT_FOLDER / file
            with open(filepath, "w") as results_file:
                writer = csv.writer(results_file)
                writer.writerow(["qualitymodel, some_model"])
                writer.writerow(["src_root, dummy_test"])
                writer.writerow(["metric", "value"])
                writer.writerow([_METRIC_NAME, 4])

    def tearDown(self):
        # shutil over os.rmdir, because it allows you to remove non/empty directories
        shutil.rmtree(_TEST_FOLDER, ignore_errors=True)

    def test_get_data_given_min_and_max_dates_returns_5(self):
        start_date = datetime.min
        end_date = datetime.max
        dashboard = Dashboard(start_date, end_date)
        data = dashboard.get_data(path=_OUTPUT_FOLDER, in_use_qm="some_model", targetPath="dummy_test")
        self.assertEqual(len(data[_METRIC_NAME]), 5)

    def test_get_data_given_2023_returns_4(self):
        start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")
        dashboard = Dashboard(start_date, end_date)
        data = dashboard.get_data(path=_OUTPUT_FOLDER, in_use_qm="some_model", targetPath="dummy_test")
        self.assertEqual(len(data[_METRIC_NAME]), 4)

    def test_get_data_given_1_day_seperation_returns_2(self):
        start_date = datetime.strptime("2023-03-02", "%Y-%m-%d")
        end_date = datetime.strptime("2023-03-03", "%Y-%m-%d")
        dashboard = Dashboard(start_date, end_date)
        data = dashboard.get_data(path=_OUTPUT_FOLDER, in_use_qm="some_model", targetPath="dummy_test")
        self.assertEqual(len(data[_METRIC_NAME]), 2)


if __name__ == "__main__":
    unittest.main()
