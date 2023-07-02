import logging
import os
import unittest

from pathlib import Path

import shutil
from core.metric.result import Result
from core.metric.violation import Violation

from core.writer import Writer

_TEST_FOLDER = Path("core") / Path("runner") / Path("test")
_OUTPUT_FOLDER = _TEST_FOLDER / Path("output")
_OUTCOMES_FOLDER = _OUTPUT_FOLDER / Path("outcomes")
_META_DATA_FOLDER = _OUTPUT_FOLDER / Path("metadata")
_VIOLATIONS_FOLDER = _OUTPUT_FOLDER / Path("violations")


class TestRunner(unittest.TestCase):
    def setUp(self):
        self._writer = Writer()
        logging.disable()

    def tearDown(self):
        # shutil over os.rmdir, because it allows you to remove non/empty directories
        shutil.rmtree(_TEST_FOLDER, ignore_errors=True)

    def test_write_to_csv_produces_non_empty_file(self):
        results = {}
        violations = [
            Violation("argument count", ("some_file", 1, 5)),
            Violation("argument count", ("some_file", 7, 15)),
        ]
        results["argument count"] = Result(
            "argument count", violations, len(violations)
        )
        self._writer.gen_output_paths_if_not_exists(_OUTPUT_FOLDER)
        self._writer.write_to_csv(results, _OUTPUT_FOLDER, "no_cpd", Path("core/"))

        self.assertEqual(len(os.listdir(_OUTCOMES_FOLDER)), 1)
        self.assertEqual(len(os.listdir(_META_DATA_FOLDER)), 1)
        self.assertEqual(len(os.listdir(_VIOLATIONS_FOLDER)), 1)

        name = Path(os.listdir(_OUTPUT_FOLDER / Path("outcomes"))[0])

        self.assertNotEqual(os.stat(_OUTCOMES_FOLDER / name).st_size, 0)
        self.assertNotEqual(os.stat(_META_DATA_FOLDER / name).st_size, 0)
        self.assertNotEqual(os.stat(_VIOLATIONS_FOLDER / name).st_size, 0)


if __name__ == "__main__":
    unittest.main()
