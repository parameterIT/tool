from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator
from byoqm.source_coordinator.query_translations import translate_to


class ReturnStatements(Metric):
    def __init__(self):
        self.coordinator: SourceCoordinator = None

    def run(self):
        count = 0
        for file in self.coordinator.src_paths:
            count += self._parse(self.coordinator.getAst(file))
        return (count, [])

    def _parse(self, ast):
        """
        Finds the amount of return statements in a file and returns the amount of functions that have more
        than 4 return statements
        """
        count = 0
        query_functions = self.coordinator.tree_sitter_language.query(
            f"""
        (_ [{translate_to[self.coordinator.language]["function"]}] @function)
        """
        )
        query_return = self.coordinator.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self.coordinator.language]["return"]}] @return)
            """
        )

        functions = query_functions.captures(ast.root_node)
        for function_node, _ in functions:
            captures = query_return.captures(function_node)
            if len(captures) > 4:
                count += 1
        return count


metric = ReturnStatements()
