import logging
import tree_sitter

from pathlib import Path
from typing import List

from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from metrics.util.query_translations import translate_to
from byoqm.source_repository.source_repository import SourceRepository


class CognitiveComplexity(Metric):
    def __init__(self):
        self._source_repository: SourceRepository | None = None

    def run(self) -> List:
        """
        A metric that counts the recursion and breaks in linear flow.

        This metric is function/method specific
        """
        violations = []
        for file_path in self._source_repository.src_root:
            violations.extend(self._count_cognitive_complexity(file_path))
        return Result("cognitive complexity", violations, len(violations))

    def _count_cognitive_complexity(self, file_path: Path):
        violations = []
        ast: tree_sitter.Tree = self._source_repository.getAst(file_path)
        lang = self._source_repository.language
        initial_nodes_query_str = f"""{translate_to[lang]["function"]} @func"""
        if lang == "c_sharp" or lang == "java":
            initial_nodes_query_str += f"""{translate_to[lang]["constructor"]} @cons"""
        query_initial_nodes = self._source_repository.tree_sitter_language.query(
            initial_nodes_query_str
        )
        initial_nodes = query_initial_nodes.captures(ast.root_node)
        for node, _ in initial_nodes:
            count = 0
            count += self._count_recursion(node, file_path)
            count += self._count_breaks_in_linear_flow(node)
            if count > 5:
                violations.append(
                    Violation(
                        "Cognitive Complexity",
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

    def _count_breaks_in_linear_flow(self, node):
        query_breaks = self._source_repository.tree_sitter_language.query(
            f"""
                ({translate_to[self._source_repository.language]["if_statement"]} @if)
                ({translate_to[self._source_repository.language]["for_statement"]} @for)
                ({translate_to[self._source_repository.language]["while_statement"]} @for)
                ({translate_to[self._source_repository.language]["catch_statement"]} @catch)
                ({translate_to[self._source_repository.language]["break_statement"]} @break)
                ({translate_to[self._source_repository.language]["continue_statement"]} @continue)
                {translate_to[self._source_repository.language]["goto"]} @goto 
            """
        )
        return len(query_breaks.captures(node))

    def _count_recursion(self, node: tree_sitter.Node, file_path):
        count = 0
        nestedFunctionCallsQuery = self._source_repository.tree_sitter_language.query(
            f"""
                {translate_to[self._source_repository.language]["invocation"]} @invocation
                """
        )
        outer_function_name = self._read_function_name(file_path, node)
        nestedCalls = nestedFunctionCallsQuery.captures(node)
        for call, _ in nestedCalls:
            try:
                name = self._read_function_name(file_path, call)
            except ValueError:
                # continue if there is no identifier, considered faulty tree_sitter parsing
                continue
            if name == outer_function_name:
                count += 1
        return count

    def _read_function_name(self, file_path: Path, node: tree_sitter.Node) -> str:
        """
        Reads the name of the function of a function_definition or call node
        """
        identifier = self._get_identifier(node)
        name_start_row = identifier.start_point[0]
        name_start_col = identifier.start_point[1]
        name_end_col = identifier.end_point[1]

        with file_path.open(
            encoding=self._source_repository.file_encodings[file_path]
        ) as f:
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
