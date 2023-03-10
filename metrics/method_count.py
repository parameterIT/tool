from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import query_lang


class MethodCount(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        for file in self.coordinator.src_paths:
            count += self._parse(self.coordinator.getAst(file))
        return count

    def _parse(self, ast):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        query = self.coordinator.language.query(
            f"""
            (_ [{query_lang[self.coordinator.prog_lang]["function"]}] @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            return 1
        return 0


metric = MethodCount()
