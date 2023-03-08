#!/usr/bin/env python
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator


class ComplexLogic(Metric):
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
        query = self._coordinator.language.query(
            """
            (_
                condition: (boolean_operator) @function.boolean_operator)
            (_
                right: (boolean_operator) @function.boolean_operator)

            """
        )
        captures = query.captures(ast.root_node)
        count = 0
        for capture in captures:
            # initial count is always at least 2 (right and left)
            boolean_count = 2
            node = capture[0]
            while node.child_by_field_name("left").type == "boolean_operator":
                boolean_count += 1
                node = node.child_by_field_name("left")
                # change the value below to a parameter when parameterizing
            if boolean_count > 2:
                count += 1
        return count


metric = ComplexLogic()
