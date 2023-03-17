from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class MethodLength(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            self._parse(self.coordinator.getAst(file), file, data)
        return data

    def _parse(self, ast, file, data):
        """
        Finds the length of all methods in a file and returns the amount of methods that have a length
        that is greater than 25
        """
        query = self.coordinator.tree_sitter_language.query(
            f"""
                (_ [{translate_to[self.coordinator.language]["function_block"]}])
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            length = (
                node.end_point[0] - node.start_point[0] + 1
            )  # length is zero indexed - therefore we add 1 at the end
            if length > 25:
                data.append(["Method Length", file, node.start_point[0]+1, node.end_point[0]])
        return


metric = MethodLength()
