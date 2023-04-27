import tree_sitter

from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.source_repository import SourceRepository
from metrics.util.language_util import (
    SUPPORTED_ENCODINGS,
    translate_to,
    SUPPORTED_LANGUAGES,
)


class MethodLength(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if (
                file_info.language in SUPPORTED_LANGUAGES
                and file_info.encoding in SUPPORTED_ENCODINGS
            ):
                violations.extend(
                    self._parse(self._source_repository.get_ast(file_info), file_info)
                )
        return Result("method length", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the length of all methods in a file and returns the amount of methods that have a length
        that is greater than 25
        """
        violations = []
        query = self._source_repository.tree_sitter_languages[file_info.language].query(
            f"""
                (_ [{translate_to[file_info.language]["function_block"]}])
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            length = (
                node.end_point[0] - node.start_point[0] + 1
            )  # length is zero indexed - therefore we add 1 at the end
            if length > 25:
                violations.append(
                    Violation(
                        "method length",
                        (
                            str(file_info.file_path),
                            node.start_point[0],
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return violations


metric = MethodLength()
