from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class MethodCount(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            self._parse(self.coordinator.getAst(file), file, data)
        return data

    def _parse(self, ast, file, data):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        query = self.coordinator.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self.coordinator.language]["function"]}] @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            data.append(["Method Count", file, 1, 1])
        return


metric = MethodCount()
