import metrics.util.parsing as parsing

from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation, Location
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class MethodLength(Metric):
    def __init__(self):
        pass

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._parse(parsing.get_ast(file_info), file_info)
                )
        return Result("method length", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the length of all methods in a file and returns the amount of methods that have a length
        that is greater than 25
        """
        violations = []
        query = parsing.LANGUAGES[file_info.language].query(
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
                location = Location(
                    file_info.file_path, node.start_point[0], node.end_point[0] + 1
                )
                violation = Violation("method length", [location])
                violations.append(violation)

        return violations


metric = MethodLength()
