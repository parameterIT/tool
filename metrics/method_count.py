from byoqm.metric.metric import Metric
from byoqm.source_repository.source_repository import SourceRepository
from byoqm.source_repository.query_translations import translate_to


class MethodCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        data = []
        for file in self._source_repository.src_paths:
            self._parse(self._source_repository.getAst(file), file, data)
        return data

    def _parse(self, ast, file, data):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        query = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["function"]}] @function)
            """
        )
        captures = query.captures(ast.root_node)
        if len(captures) > 20:
            data.append(
                [
                    "Method Count",
                    file,
                    str(captures[0][0].start_point[0] + 1),
                    str(captures[len(captures) - 1][0].end_point[0]),
                ]
            )
        return


metric = MethodCount()
