from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Location, Violation
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class ArgumentCount(Metric):
    def __init__(self):
        pass

    def run(self):
        violations = []
        for file, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._parse(self._source_repository.get_ast(file_info), file_info)
                )
        return Result("argument count", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the number of functions that have more than 4 parameters
        """
        violations = []
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        query = tree_sitter_language.query(
            f"""
            (_ [{translate_to[file_info.language]["parameters"]}] @parameters)
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            if node.named_child_count > 4:
                location = Location(
                    file_info.file_path, node.start_point[0] + 1, node.end_point[0] + 1
                )
                violation = Violation("argument count", [location])
                violations.append(violation)

        return violations


metric = ArgumentCount()
