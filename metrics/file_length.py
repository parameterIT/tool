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
        for file in self._source_repository.src_paths:
            violations = []
            encoding = self._source_repository.file_encodings[file]
            with open(file, encoding=encoding) as f:
                violations.extend(
                    self._parse(f, self._source_repository.getAst(file), file)
                )
                result.outcome = len(result.violations)
                result = Result("file length", violations, len(violations))
        return result

    def _parse(self, file, ast, path):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["comment"]}] @comment)
            """
        )
        captures = query.captures(ast.root_node)
        count_comments = 0
        for node, _ in captures:
            count_comments += (
                node.end_point[0] - node.start_point[0]
            ) + 1  # length is zero indexed - therefore we add 1 at the end
        loc = sum(1 for line in file if line.rstrip()) - count_comments
        if loc > 250:
            violations.append(Violation("LOC", (str(path), -1, -1)))
        return violations


metric = FileLength()
