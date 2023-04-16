from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class MethodCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for file, file_info in self._source_repository.files.items():
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
                    "Method Count",
                    (
                        str(file_info.file_path),
                        captures[0][0].start_point[0] + 1,
                        captures[len(captures) - 1][0].end_point[0],
                    ),
                )
            )
        return violations


metric = MethodCount()
