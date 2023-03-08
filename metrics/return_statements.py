#!/usr/bin/env python
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator


class ReturnStatements(Metric):
    def __init__(self):
        self._coordinator = None

    def set_coordinator(self, coordinator: SourceCoordinator):
        self._coordinator = coordinator

    def run(self):
        count = 0
        for file in self._coordinator.src_paths:
            count += self._parse(self._coordinator.getAst(file))
        return count

    def _parse(self, ast):
        count = 0
        query_functions = self._coordinator.language.query(
            """
        (_ (function_definition) @function)
        """
        )
        query_return = self._coordinator.language.query(
            """
            (_ (return_statement) @return)
            """
        )

        functions = query_functions.captures(ast.root_node)
        for function_node, _ in functions:
            captures = query_return.captures(function_node)
            if len(captures) > 4:
                count += 1
        return count


metric = ReturnStatements()
