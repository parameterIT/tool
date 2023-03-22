from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from byoqm.source_repository.query_translations import translate_to


class ArgumentCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        result = Result("argument count", [])
        for file in self._source_repository.src_paths:
            self._parse(self._source_repository.getAst(file), result, file)
        return result

    def _parse(self, ast, result, file):
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
                result.append(
                    Violation(
                        "argument count",
                        (
                            str(file),
                            node.start_point[0] + 1,
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return


metric = ArgumentCount()
