import logging
import unittest

from pathlib import Path

from test.test_support import shutil

from byoqm.runner import Runner

_TEST_FOLDER = Path("byoqm/runner/test")
_OUTPUT_FOLDER = _TEST_FOLDER / Path("test")
_OUTCOMES_FOLDER = _OUTPUT_FOLDER / Path("outcomes")
_VIOLATION_FOLDER = _OUTPUT_FOLDER / Path("violations")


class TestRunner(unittest.TestCase):
    def setUp(self):
        _OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        _OUTCOMES_FOLDER.mkdir(parents=True, exist_ok=True)
        _VIOLATION_FOLDER.mkdir(parents=True, exist_ok=True)
        self._runner = Runner("no_cpd", Path("byoqm/"), "python")
        logging.disable()

    def test_load_given_code_climate_inits_runner(self):
        self._runner._load("code_climate")
        # Not crashing on the above line, means that code_climate was successfully located
        # and found, so assert true
        self.assertTrue(True)

    def test_load_given_the_non_existent_model_raises_FileNotFoundError(self):
        self.assertRaises(
            FileNotFoundError,
            self._runner._load,
            "this model has never, does not, and will never exist (hopefully)",
        )


if __name__ == "__main__":
    unittest.main()
