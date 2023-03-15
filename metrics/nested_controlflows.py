from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class NestedControlflows(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        for file in self.coordinator.src_paths:
            count += self._parse(self.coordinator.getAst(file))
        return count

    def _unique(self, not_unique_list):
        unique_list = []

        for x in not_unique_list:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    def _parse(self, ast) -> int:
        """
        Finds the control statements of a file and returns the amount of control statements that have a nested
        control flow depth of at least 4
        """
        count = 0

        query = self.coordinator.tree_sitter_language.query(
            translate_to[self.coordinator.language]["nested_controlflow1"]
        )
        inital_nodes = self._unique(query.captures(ast.root_node))
        sub_node_query = self.coordinator.tree_sitter_language.query(
            translate_to[self.coordinator.language]["nested_controlflow2"]
        )
        for node, _ in inital_nodes:
            found = False
            nodes2 = sub_node_query.captures(node)
            for node2, _ in nodes2:
                if found:
                    break
                nodes3 = sub_node_query.captures(node2)
                for node3, _ in nodes3:
                    if found:
                        break
                    if len(sub_node_query.captures(node3)) > 0:
                        count += 1
                        found = True

        return count


metric = NestedControlflows()
