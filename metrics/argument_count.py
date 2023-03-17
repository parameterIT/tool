from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository, translate_to


class ArgumentCount(Metric):
    def __init__(self):
        self.coordinator: SourceRepository = None

    def run(self):
        data = []
        for file in self.coordinator.src_paths:
            self._parse(self.coordinator.getAst(file), data, file)
        return data

    def _parse(self, ast, data, file):
        """
        Finds the number of functions that have more than 4 parameters
        """
        query = self.coordinator.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self.coordinator.language]["parameters"]}] @parameters)
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            if node.named_child_count > 4:
                data.append(["Argument Count", file, 1, 1])
        return


metric = ArgumentCount()
