from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator


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
        count = 0
        query = self.coordinator.language.query(
            """
                (module [
                (if_statement 
                    consequence: (block) @cons
                        )
                (if_statement 
                    consequence: (block) @cons
                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                        )
                (while_statement body: (block) @cons)
                (for_statement body: (block) @cons)]
                )
                
                (function_definition
                body: (block [
                    (if_statement 
                        consequence: (block) @cons
                            )
                    (if_statement 
                        consequence: (block) @cons
                        alternative: (_ [body: (block) consequence: (block)] @cons)
                            )
                    (while_statement body: (block) @cons)
                    (for_statement body: (block) @cons)])
                )
                    """
        )
        inital_nodes = self._unique(query.captures(ast.root_node))
        sub_node_query = self.coordinator.language.query(
            """
                (_ [
                (if_statement 
                    consequence: (block) @cons
                        )
                (if_statement 
                    consequence: (block) @cons
                    alternative: (_ [body: (block) consequence: (block) ] @cons) 
                        )
                (while_statement body: (block) @cons)
                (for_statement body: (block) @cons)]
                )
                    """
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
