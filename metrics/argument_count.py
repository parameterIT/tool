from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class ArgumentCount(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            self._parse(self.coordinator.getAst(file), data, file)
        return data

    def _parse(self, ast, data, file):
        """
        Finds the number of functions that have more than 4 parameters
        """
        query = self.coordinator.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self.coordinator.language]["parameters"]}] @parameters)
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            if node.named_child_count > 4:
                data.append(
                    ["Argument Count", file, node.start_point[0] + 1, node.end_point[0]]
                )
        return


metric = ArgumentCount()
