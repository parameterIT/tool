import os
import unittest

from pathlib import Path
from byoqm.metric.metric import Metric

from byoqm.source_repository.source_repository import SourceRepository
from metrics.breaks_in_linear_flow import BreaksInLinearFlow


class TestBreaksInLinearFlow(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository: SourceRepository = SourceRepository(
            Path("./metrics/test/data/test_data_breaks_in_linear_flow"), "python"
        )
        self._metric: Metric = BreaksInLinearFlow()
        self._metric._source_repository = self._source_repository

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())

    def test_run_given_python_file_returns_5(self):
        expected = 5
        actual = len(self._metric.run())
        self.assertEqual(expected, actual)
