from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import query_lang


class FileLength(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        for file in self.coordinator.src_paths:
            with open(file) as f:
                count += self._parse(f,self.coordinator.getAst(file))
        return count

    def _parse(self, file, ast):
        """
        Finds out whether or not a file is more than 250 lines long
        """
        query = self.coordinator.language.query(
            f"""
            (_ [{query_lang[self.coordinator.prog_lang]["comment"]}] @comment)
            """
        )
        captures = query.captures(ast.root_node)
        count_comments = 0
        for node in captures:
            n = node[0]
            count_comments += (
                (n.end_point[0] - n.start_point[0]) + 1
            )  # length is zero indexed - therefore we add 1 at the end
        loc = sum(1 for line in file if line.rstrip()) - count_comments
        if loc > 250:
            return 1
        return 0


metric = FileLength()
