import logging
import tree_sitter

from pathlib import Path
from typing import List

from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.file_info import FileInfo
from metrics.util.query_translations import translate_to
from modu.source_repository.source_repository import SourceRepository


class CognitiveComplexity(Metric):
    def __init__(self):
        self._source_repository: SourceRepository | None = None

    def run(self) -> Result:
        """
        A metric that counts the recursion and breaks in linear flow.

        This metric is function/method specific
        """
        violations = []
        for file_path, file_info in self._source_repository.files.items():
            violations.extend(self._count_cognitive_complexity(file_path, file_info))
        return Result("cognitive complexity", violations, len(violations))

    def _count_cognitive_complexity(self, file_path: Path, file_info: FileInfo):
        violations = []
        ast: tree_sitter.Tree = self._source_repository.get_ast(file_info)
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]

        initial_nodes_query_str = (
            f"""{translate_to[file_info.language]["function"]} @func"""
        )
        if file_info.language == "c_sharp" or file_info.language == "java":
            initial_nodes_query_str += (
                f"""{translate_to[file_info.language]["constructor"]} @cons"""
            )
        query_initial_nodes = tree_sitter_language.query(initial_nodes_query_str)

        initial_nodes = query_initial_nodes.captures(ast.root_node)
        for node, _ in initial_nodes:
            count = 0
            count += self._count_recursion(node, file_info)
            count += self._count_breaks_in_linear_flow(node, file_info)
            if count > 5:
                violations.append(
                    Violation(
                        "cognitive complexity",
                        # We use start_point for what would otherwise be start_line & end_line
                        # to report the line where the keyword that breaks linear flow is met .
                        (
                            str(file_path),
                            node.start_point[0] + 1,
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return violations

    def _count_breaks_in_linear_flow(self, node, file_info):
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        query_breaks = tree_sitter_language.query(
            f"""
                ({translate_to[file_info.language]["if_statement"]} @if)
                ({translate_to[file_info.language]["for_statement"]} @for)
                ({translate_to[file_info.language]["while_statement"]} @for)
                ({translate_to[file_info.language]["catch_statement"]} @catch)
                ({translate_to[file_info.language]["break_statement"]} @break)
                ({translate_to[file_info.language]["continue_statement"]} @continue)
                {translate_to[file_info.language]["goto"]} @goto 
            """
        )
        return len(query_breaks.captures(node))

    def _count_recursion(self, node: tree_sitter.Node, file_info):
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]

        count = 0
        nested_function_calls_query = tree_sitter_language.query(
            f"""
                {translate_to[file_info.language]["invocation"]} @invocation
                """
        )
        outer_function_name = self._read_function_name(file_info, node)
        nested_calls = nested_function_calls_query.captures(node)
        for call, _ in nested_calls:
            try:
                name = self._read_function_name(file_info, call)
            except ValueError:
                # continue if there is no identifier, considered faulty tree_sitter parsing
                continue
            if name == outer_function_name:
                count += 1
        return count

    def _read_function_name(self, file_info: FileInfo, node: tree_sitter.Node) -> str:
        """
        Reads the name of the function of a function_definition or call node
        """
        identifier = self._get_identifier(node)
        name_start_row = identifier.start_point[0]
        name_start_col = identifier.start_point[1]
        name_end_col = identifier.end_point[1]

        with file_info.file_path.open(encoding=file_info.encoding) as f:
            range_length = name_start_row
            for _ in range(
                range_length
            ):  # Skip the lines leading up to the line needed
                f.readline()
            line = f.readline()

            return line[name_start_col:name_end_col]

    def _get_identifier(self, node: tree_sitter.Node) -> tree_sitter.Node:
        for child in node.children:
            if child.type == "identifier":
                return child
        raise ValueError(f"{node} has no children of the type identifier")


metric = CognitiveComplexity()
