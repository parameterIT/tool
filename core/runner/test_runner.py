import logging
import unittest

from pathlib import Path

from core.runner import Runner


class TestRunner(unittest.TestCase):
    def setUp(self):
        self._runner = Runner("no_cpd", Path("core/"))
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
