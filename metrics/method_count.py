from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class MethodCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        result = Result("method count", [])
        for file in self._source_repository.src_paths:
            result.violations.extend(
                self._parse(self._source_repository.getAst(file), file)
            )
        return result

    def _parse(self, ast, file):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        violations = []
        function_block = translate_to[self._source_repository.language]["function"]
        if not self._source_repository.language == "python":
            function_block += translate_to[self._source_repository.language][
                "constructor"
            ]

        query = self._source_repository.tree_sitter_language.query(
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
                        str(file),
                        captures[0][0].start_point[0] + 1,
                        captures[len(captures) - 1][0].end_point[0],
                    ),
                )
            )
        return violations


metric = MethodCount()
