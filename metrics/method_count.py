from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator


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
            """
            (_ (function_definition) @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            return 1
        return 0


metric = MethodCount()
