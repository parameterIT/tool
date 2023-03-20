import tree_sitter

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
        return results

    def _run_on_file(self, file_path: Path):
        results = []
        ast = self._source_repository.getAst(file_path)

        functionsQuery = self._source_repository.tree_sitter_language.query(
            f"""
            {translate_to["python"]["function"]} @function
            """
        )
        functions = functionsQuery.captures(ast.root_node)

        nestedFunctionCallsQuery = self._source_repository.tree_sitter_language.query(
            f"""
                {translate_to["python"]["nested_function_call"]}
                """
        )
        for node, _ in functions:
            try:
                outer_function_name = self._read_function_name(file_path, node)
            except ValueError:
                # pass if there is no identifier, considered faulty tree_sitter parsing
                continue

            nestedCalls = nestedFunctionCallsQuery.captures(node)
            for call, _ in nestedCalls:
                try:
                    name = self._read_function_name(file_path, call)
                except ValueError:
                    # pass if there is no identifier, considered faulty tree_sitter parsing
                    continue
                if name == outer_function_name:
                    results.append(["Recursion", file_path, 1, 1])

        return results

    def _read_function_name(self, file_path: Path, node: tree_sitter.Node) -> str:
        """
        Reads the name of the function of a function_definition or call node
        """
        identifer = self._get_identifier(node)

        name_start_row = identifer.start_point[0]
        name_start_col = identifer.start_point[1]
        name_end_col = identifer.end_point[1]

        with file_path.open() as f:
            for _ in range(name_start_row - 1):
                # Skip the first row-1 lines
                f.readline()

            line = f.readline()
            return line[name_start_col:name_end_col]

    def _get_identifier(self, node: tree_sitter.Node) -> tree_sitter.Node:
        for child in node.children:
            if child.type == "identifier":
                return child
        raise ValueError(f"{node} has no children of the type identifier")


metric = Recursion()
