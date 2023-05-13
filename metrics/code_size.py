from typing import List
from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import (
    translate_to,
    SUPPORTED_LANGUAGES,
    SUPPORTED_ENCODINGS,
)


class CodeSize(Metric):
    """
    CodeSize measures the total lines of code, exlcuding comments, of the source code.
    """

    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        loc: int = 0
        for file, file_info in self._source_repository.files.items():
            if (
                file_info.language in SUPPORTED_LANGUAGES
                and file_info.encoding in SUPPORTED_ENCODINGS
            ):
                with open(file, encoding=file_info.encoding) as f:
                    loc = loc + self._parse(
                        f, file_info, self._source_repository.get_ast(file_info)
                    )
        return loc

    def _parse(self, open_file, file_info, ast):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
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
        return loc


metric = CodeSize()
