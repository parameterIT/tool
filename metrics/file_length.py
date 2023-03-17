from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository, translate_to


class FileLength(Metric):
    def __init__(self):
        self.coordinator: SourceRepository = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            with open(file) as f:
                self._parse(f, self.coordinator.getAst(file), file, data)
        return data

    def _parse(self, file, ast, path, data):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
        query = self.coordinator.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self.coordinator.language]["comment"]}] @comment)
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
            data.append(["LOC", path, -1, -1])
        return


metric = FileLength()
