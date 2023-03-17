from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from byoqm.source_repository.query_translations import translate_to


class ArgumentCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        data = []
        for file in self._source_repository.src_paths:
            self._parse(self._source_repository.getAst(file), data, file)
        return data

    def _parse(self, ast, data, file):
        """
        Finds the number of functions that have more than 4 parameters
        """
        query = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["parameters"]}] @parameters)
            """
        )
        captures = query.captures(ast.root_node)
        for node, _ in captures:
            if node.named_child_count > 4:
                data.append(
                    ["Argument Count", file, str(node.start_point[0] + 1), str(node.end_point[0])]
                )
        return


metric = ArgumentCount()
