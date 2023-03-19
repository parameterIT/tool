import logging

from pathlib import Path

from test.test_support import sys
from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from byoqm.source_repository.query_translations import translate_to


class Recursion(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        results = []
        for file_path in self._source_repository.src_paths:
            results.extend(self._run_on_file(file_path))

    def _run_on_file(self, file_path: Path):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.WARNING)
        logging.getLogger().addHandler(handler)

        ast = self._source_repository.getAst(file_path)

        functionsQuery = self._source_repository.tree_sitter_language.query(
            f"""
            {translate_to["python"]["function"]} @function
            """
        )
        functions = functionsQuery.captures(ast.root_node)
        for function, _ in functions:
            logging.warning(function.children)

        nestedFunctionCallsQuery = self._source_repository.tree_sitter_language.query(
            f"""
                {translate_to["python"]["nested_function_call"]}
                """
        )
        logging.warning("warning")
        for node, _ in functions:
            nestedCalls = nestedFunctionCallsQuery.captures(node)
            for call in nestedCalls:
                logging.warn(call)

        return functions
