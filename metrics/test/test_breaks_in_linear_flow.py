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
        expected = 7
        result = self._metric.run()
        actual = result.get_frequency()
        self.assertEqual(actual,expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1],locations[0][2]),(1,1))
