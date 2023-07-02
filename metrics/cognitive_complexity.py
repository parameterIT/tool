import logging
import tree_sitter

from pathlib import Path
from typing import List

from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation, Location
from core.source_repository.file_info import FileInfo
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES
from core.source_repository.source_repository import SourceRepository


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
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._count_cognitive_complexity(file_path, file_info)
                )
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
            count += self._count_nesting(node, file_info)
            if count > 5:
                location = Location(file_info.file_path, node.start_point[0], node.end_point[1])
                violation = Violation("cognitive_complexity", [location])
                violations.append(violation)
                
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

    def _count_nesting(self, node, file_info):
        count = 0
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        initial_query_str = translate_to[file_info.language]["method_control_flow"]
        if file_info.language == "c_sharp" or file_info.language == "java":
            initial_query_str += translate_to[file_info.language][
                "constructor_control_flow"
            ]
        initial_query = tree_sitter_language.query(initial_query_str)
        subsequent_query = tree_sitter_language.query(
            translate_to[file_info.language]["nested_controlflow_subsequent_nodes"]
        )
        initial_nodes = initial_query.captures(node)

        for second_nested_node, _ in initial_nodes:
            found = False
            nodes2 = subsequent_query.captures(second_nested_node)
            for third_nested_node, _ in nodes2:
                if found:
                    break
                if len(subsequent_query.captures(third_nested_node)) > 0:
                    count += 1
                    found = True
        return count


metric = CognitiveComplexity()
