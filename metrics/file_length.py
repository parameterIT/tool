from io import TextIOWrapper
from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class FileLength(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for file, file_info in self._source_repository.files.items():
            with open(file, encoding=file_info.encoding) as f:
                violations.extend(
                    self._parse(
                        f, self._source_repository.get_ast(file_info), file_info
                    )
                )
        return Result("file length", violations, len(violations))

    def _parse(self, open_file, ast, file_info):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
        violations = []
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]

        query = tree_sitter_language.query(
            f"""
            (_ [{translate_to[file_info.language]["comment"]}] @comment)
            """
        )
        captures = query.captures(ast.root_node)
        count_comments = 0
        for node, _ in captures:
            count_comments += (
                node.end_point[0] - node.start_point[0]
            ) + 1  # length is zero indexed - therefore we add 1 at the end
        loc = sum(1 for line in open_file if line.rstrip()) - count_comments
        if loc > 250:
            violations.append(Violation("LOC", (str(file_info.file_path), -1, -1)))
        return violations


metric = FileLength()
