from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository, translate_to


class ReturnStatements(Metric):
    def __init__(self):
        self.coordinator: SourceRepository = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            self._parse(self.coordinator.getAst(file), file, data)
        return data

    def _parse(self, ast, file, data):
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
        for node, _ in functions:
            captures = query_return.captures(node)
            if len(captures) > 4:
                data.append(["Return Statements", file, 1, 1])
        return


metric = ReturnStatements()
