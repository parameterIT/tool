import unittest

from pathlib import Path

from test.test_support import os, shutil

from byoqm.runner import Runner

_TEST_FOLDER = Path("byoqm/runner/test")
_OUTPUT_FOLDER = _TEST_FOLDER / Path("test")


class TestRunner(unittest.TestCase):
    def setUp(self):
        _OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

        self._runner = Runner("no_cpd", Path("byoqm/"), _OUTPUT_FOLDER, True, "python")

    def tearDown(self):
        # shutil over os.rmdir, because it allows you to remove non/empty directories
        shutil.rmtree(_TEST_FOLDER, ignore_errors=True)

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

    def test_run_produces_non_empty_file(self):
        output = self._runner.run()
        self.assertTrue(output.stat().st_size > 0)


if __name__ == "__main__":
    unittest.main()
