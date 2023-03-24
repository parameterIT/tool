import tree_sitter

from pathlib import Path
from typing import List

from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.query_translations import translate_to
from byoqm.source_repository.source_repository import SourceRepository


class BreaksInLinearFlow(Metric):
    def __init__(self):
        self._source_repository: SourceRepository | None = None

    def run(self) -> List:
        """
        Counts the number of occurences of looping strucctures and conditional
        structures
        """
        result = Result("breaks in linear flow", [])
        for file_path in self._source_repository.src_paths:
            result.violations.extend(self._count_control_flow_statement(file_path))
        return result

    def _count_control_flow_statement(self, file_path: Path):
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            f"""
            [
                ({translate_to[self._source_repository.language]["if_statement"]} @if)
                ({translate_to[self._source_repository.language]["for_statement"]} @for)
                ({translate_to[self._source_repository.language]["while_statement"]} @for)
                ({translate_to[self._source_repository.language]["catch_statement"]} @catch)
                ({translate_to[self._source_repository.language]["break_statement"]} @break)
                ({translate_to[self._source_repository.language]["continue_statement"]} @continue)
            ]
            """
        )
        ast: tree_sitter.Tree = self._source_repository.getAst(file_path)
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            violations.append(
                Violation(
                    "breaks in linear flow",
                    # We use start_point for what would otherwise be start_line & end_line
                    # to report the line where the keyword that breaks linear flow is met .
                    (str(file_path), node.start_point[0] + 1, node.start_point[0] + 1),
                )
            )
        return violations


metric = BreaksInLinearFlow()
