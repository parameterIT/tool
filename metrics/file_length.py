from io import TextIOWrapper
from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from byoqm.source_repository.query_translations import translate_to
import chardet


class FileLength(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        result = Result("file length", [])
        for file in self._source_repository.src_paths:
            encoding = 'utf-8'
            with open(file, "rb") as f:
                encoding = chardet.detect(f.read())["encoding"]
            with open(file, encoding=encoding) as f:
                result.violations.extend(
                    self._parse(f, self._source_repository.getAst(file), file)
                )
        return result

    def _parse(self, file : TextIOWrapper, ast, path):
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
