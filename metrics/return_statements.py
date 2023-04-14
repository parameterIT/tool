from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class ReturnStatements(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for file in self._source_repository.src_paths:
            violations.extend(self._parse(self._source_repository.getAst(file), file))
        return Result("Return Statements", violations, len(violations))

    def _parse(self, ast, file):
        """
        Finds the amount of return statements in a file and returns the amount of functions that have more
        than 4 return statements
        """
        violations = []
        query_functions = self._source_repository.tree_sitter_language.query(
            f"""
        (_ [{translate_to[self._source_repository.language]["function"]}] @function)
        """
        )
        query_return = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["return"]}] @return)
            """
        )

        functions = query_functions.captures(ast.root_node)
        for node, _ in functions:
            captures = query_return.captures(node)
            if len(captures) > 4:
                violations.append(
                    Violation(
                        "Return Statements",
                        (
                            str(file),
                            node.start_point[0] + 1,
                            node.end_point[0] + 1,
                        ),
                    )
                )
        return violations


metric = ReturnStatements()
