from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class FileLength(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        data = []
        for file in self.coordinator.src_paths:
            with open(file) as f:
                count += self._parse(f, self.coordinator.getAst(file))
                data.append(["LOC",file, -1,-1])
        return (count,data)

    def _parse(self, file, ast):
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
        for node in captures:
            n = node[0]
            count_comments += (
                n.end_point[0] - n.start_point[0]
            ) + 1  # length is zero indexed - therefore we add 1 at the end
        loc = sum(1 for line in file if line.rstrip()) - count_comments
        if loc > 250:
            return 1
        return 0


metric = FileLength()
