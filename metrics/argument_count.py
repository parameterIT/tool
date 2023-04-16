from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class ArgumentCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for file, file_info in self._source_repository.files.items():
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
                violations.append(
                    Violation(
                        "argument count",
                        (
                            str(file_info.file_path),
                            node.start_point[0] + 1,
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return violations


metric = ArgumentCount()
