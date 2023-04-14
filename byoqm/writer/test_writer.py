import logging
import os
import unittest

from pathlib import Path

from test.test_support import shutil
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation

from byoqm.writer import Writer

_TEST_FOLDER = Path("byoqm/runner/test")
_OUTPUT_FOLDER = _TEST_FOLDER / Path("test")
_FREQUENCY_FOLDER = _OUTPUT_FOLDER / Path("frequencies")
_META_DATA_FOLDER = _OUTPUT_FOLDER / Path("metadata")
_VIOLATIONS_FOLDER = _OUTPUT_FOLDER / Path("violations")


class TestRunner(unittest.TestCase):
    def setUp(self):
        self._writer = Writer()
        logging.disable()

    def tearDown(self):
        # shutil over os.rmdir, because it allows you to remove non/empty directories
        shutil.rmtree(_TEST_FOLDER, ignore_errors=True)

    def test_run_produces_non_empty_file(self):
        results = {}
        results["argument count"] = Result(
            "argument count",
            [
                Violation("argument count", ("some_file", 1, 5)),
                Violation("argument count", ("some_file", 7, 15)),
            ],
        )
        self._writer.run(results, _OUTPUT_FOLDER, "no_cpd", Path("byoqm/"))

        self.assertEqual(len(os.listdir(_FREQUENCY_FOLDER)), 1)
        self.assertEqual(len(os.listdir(_META_DATA_FOLDER)), 1)
        self.assertEqual(len(os.listdir(_VIOLATIONS_FOLDER)), 1)

        name = Path(os.listdir(_OUTPUT_FOLDER / Path("frequencies"))[0])

        self.assertNotEqual(os.stat(_FREQUENCY_FOLDER / name).st_size, 0)
        self.assertNotEqual(os.stat(_META_DATA_FOLDER / name).st_size, 0)
        self.assertNotEqual(os.stat(_VIOLATIONS_FOLDER / name).st_size, 0)


if __name__ == "__main__":
    unittest.main()
