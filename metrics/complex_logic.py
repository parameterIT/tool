from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class ComplexLogic(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        for file in self.coordinator.src_paths:
            count += self._parse(self.coordinator.getAst(file))
        return count

    def _parse(self, ast):
        """
        Finds the conditionals of a file and returns the number of conditionals that have more than 4 conditions
        """
        count = 0
        query = self.coordinator.language.query(
            f"""
            (_ [{translate_to[self.coordinator.prog_lang]["bool_operator"]}] @bool_operator)
            """
        )
        captures = query.captures(ast.root_node)
        count = 0
        for capture in captures:
            # initial count is always at least 2 (right and left)
            boolean_count = 2
            node = capture[0]
            bool_operator = translate_to[self.coordinator.prog_lang][
                "bool_operator_child"
            ]
            children = [
                node.child_by_field_name("left"),
                node.child_by_field_name("right"),
            ]
            while len(children) > 0:
                if boolean_count > 4:
                    break
                child = children.pop()
                if child.type == bool_operator:
                    boolean_count += 1
                    children.extend(
                        [
                            child.child_by_field_name("left"),
                            child.child_by_field_name("right"),
                        ]
                    )
            if boolean_count > 4:
                count += 1
        return count


metric = ComplexLogic()
