import unittest
import os

from pathlib import Path

from byoqm.source_repository.source_repository import SourceRepository
from metrics.recursion import Recursion


class TestRecursion(unittest.TestCase):
    def setUp(self):
        # chdir because paths are assumed to be relative from the project root but test
        # paths start at the test file
        os.chdir("../../")
        self._source_repository = SourceRepository(
            Path("./metrics/test/data/test_data_recursion"), "python"
        )
        self._metric = Recursion()
        self._metric._source_repository = self._source_repository

    def tearDown(self):
        os.chdir(Path("metrics/test").resolve())

    def test_recursion_given_recursion_file_returns_1(self):
        result = self._metric.run()
        actual = result.get_frequency()
        expected = 1
        self.assertEqual(actual, expected)
        locations = result.get_violation_locations()
        self.assertEqual((locations[0][1],locations[0][2]),(1,1))
