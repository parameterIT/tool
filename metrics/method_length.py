from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class MethodLength(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        for file in self._source_repository.src_paths:
            violations = []
            violations.extend(
                self._parse(self._source_repository.getAst(file), file)
            )
        return Result("method length", violations, len(violations))

    def _parse(self, ast, file):
        """
        Finds the length of all methods in a file and returns the amount of methods that have a length
        that is greater than 25
        """
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            f"""
                (_ [{translate_to[self._source_repository.language]["function_block"]}])
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
                        (str(file), node.start_point[0], node.end_point[0] + 1),
                    )
                )
        return violations


metric = MethodLength()
