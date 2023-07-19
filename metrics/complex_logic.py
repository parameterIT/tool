import metrics.util.parsing as parsing

from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Location, Violation
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class ComplexLogic(Metric):
    def __init__(self):
        pass

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(self._parse(parsing.get_ast(file_info), file_info))
        return Result("complex logic", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the conditionals of a file and returns the number of conditionals that have more than 4 conditions
        """
        violations = []
        tree_sitter_language = parsing.LANGUAGES[file_info.language]

        query = tree_sitter_language.query(
            f"""
            (_ [{translate_to[file_info.language]["bool_operator"]}] @bool_operator)
            """
        )
        captures = query.captures(ast.root_node)
        for capture in captures:
            # initial count is always at least 2 (right and left)
            boolean_count = 2
            node = capture[0]
            bool_operator = translate_to[file_info.language]["bool_operator_child"]
            children = [
                node.child_by_field_name("left"),
                node.child_by_field_name("right"),
            ]
            while len(children) > 0:
                if boolean_count > 4:
                    break
                child = children.pop()
                if child.type == bool_operator:
                    boolean_count += 1
                    children.extend(
                        [
                            child.child_by_field_name("left"),
                            child.child_by_field_name("right"),
                        ]
                    )
            if boolean_count > 4:
                location = Location(
                    file_info.file_path, node.start_point[0] + 1, node.end_point[0] + 1
                )
                violation = Violation("complex logic", [location])
                violations.append(violation)

        return violations


metric = ComplexLogic()
