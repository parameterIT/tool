import metrics.util.parsing as parsing

from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation, Location, Location
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class ReturnStatements(Metric):
    def __init__(self):
        pass

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._parse(parsing.get_ast(file_info), file_info)
                )
        return Result("Return Statements", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the amount of return statements in a file and returns the amount of functions that have more
        than 4 return statements
        """
        violations = []
        tree_sitter_language = parsing.LANGUAGES[
            file_info.language
        ]
        query_functions = tree_sitter_language.query(
            f"""
        (_ [{translate_to[file_info.language]["function"]}] @function)
        """
        )
        query_return = tree_sitter_language.query(
            f"""
            (_ [{translate_to[file_info.language]["return"]}] @return)
            """
        )

        functions = query_functions.captures(ast.root_node)
        for node, _ in functions:
            captures = query_return.captures(node)
            if len(captures) > 4:
                location = Location(
                    file_info.file_path, node.start_point[0] + 1, node.end_point[0] + 1
                )
                violation = Violation("return statements", [location])
                violations.append(violation)

        return violations


metric = ReturnStatements()
