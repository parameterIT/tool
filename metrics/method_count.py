#!/usr/bin/env python
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator

class MethodCount(Metric):
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
            (_ (function_definition) @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            count += 1
        return count
    
metric = MethodCount()