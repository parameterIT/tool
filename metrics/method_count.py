from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.source_repository import SourceRepository
from metrics.util.language_util import (
    SUPPORTED_ENCODINGS,
    translate_to,
    SUPPORTED_LANGUAGES,
)


class MethodCount(Metric):
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
        return Result("method count", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        violations = []
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        function_block = translate_to[file_info.language]["function"]
        if not file_info.language == "python":
            function_block += translate_to[file_info.language]["constructor"]

        query = tree_sitter_language.query(
            f"""
            (_ [{function_block}] @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            violations.append(
                Violation(
                    "method count",
                    (
                        str(file_info.file_path),
                        captures[0][0].start_point[0] + 1,
                        captures[len(captures) - 1][0].end_point[0],
                    ),
                )
            )
        return violations


metric = MethodCount()
