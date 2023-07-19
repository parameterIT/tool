import metrics.util.parsing as parsing

from io import TextIOWrapper
from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation, Location
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import (
    translate_to,
    SUPPORTED_LANGUAGES,
    SUPPORTED_ENCODINGS,
)


class FileLength(Metric):
    def __init__(self):
        pass

    def run(self):
        violations = []
        for file, file_info in self._source_repository.files.items():
            if (
                file_info.language in SUPPORTED_LANGUAGES
                and file_info.encoding in SUPPORTED_ENCODINGS
            ):
                with open(file, encoding=file_info.encoding) as f:
                    violations.extend(
                        self._parse(
                            f, parsing.get_ast(file_info), file_info
                        )
                    )
        return Result("file length", violations, len(violations))

    def _parse(self, open_file, ast, file_info):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
        violations = []
        tree_sitter_language = parsing.LANGUAGES[
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
            location = Location(file_info.file_path, -1, -1)
            violation = Violation("LOC", [location])
            violations.append(violation)

        return violations


metric = FileLength()
