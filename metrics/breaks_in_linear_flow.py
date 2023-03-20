import tree_sitter

from pathlib import Path
from typing import List

from byoqm.metric.metric import Metric
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
        results = []
        for file_path in self._source_repository.src_paths:
            results.extend(self._count_control_flow_statement(file_path))
        return results

    def _count_control_flow_statement(self, file_path: Path):
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
        results = [("Breaks In Linear Flow", file_path, 1, 1) for _, _ in captures]
        return results


metric = BreaksInLinearFlow()
