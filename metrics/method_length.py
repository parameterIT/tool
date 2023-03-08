#!/usr/bin/env python
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator

class MethodLength(Metric):
    def __init__(self):
        self._coordinator = None

    def set_coordinator(self, coordinator : SourceCoordinator):
        self._coordinator = coordinator

    def run(self):
        count = 0
        for file in self._coordinator.src_paths:
            count += self._parse(self._coordinator.getAst(file))
        return count


    def _parse(self,ast):
        count = 0
        query = self._coordinator.language.query(
        """
                (function_definition
                    body: (block) @function.block)
                """
        )
        captures = query.captures(ast.root_node)
        for node in captures:
            n = node[0]
            length = (
                n.end_point[0] - n.start_point[0] + 1
            )  # length is zero indexed - therefore we add 1 at the end
            if length > 25:
                count += 1
        return count

metric = MethodLength()