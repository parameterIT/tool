from modu.metric.metric import Metric
from modu.metric.result import Result
from modu.metric.violation import Violation
from modu.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class CodeSize(Metric):
    """
    CodeSize measures the total lines of code, exlcuding comments, of the source code.
    """

    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        loc: int = 0
        for file, file_info in self._source_repository.files.items():
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
