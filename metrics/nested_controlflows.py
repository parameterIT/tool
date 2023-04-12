from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to


class NestedControlflows(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        result = Result("nested controlflow", [])
        for file in self._source_repository.src_paths:
            result.violations.extend(
                self._parse(self._source_repository.getAst(file), file)
            )
        return result

    def _unique(self, not_unique_list):
        unique_list = []

        for x in not_unique_list:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    def _parse(self, ast, file):
        """
        Finds the control statements of a file and returns the amount of control statements that have a nested
        control flow depth of at least 4
        """
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            translate_to[self._source_repository.language][
                "nested_controlflow_initial_nodes"
            ]
        )
        inital_nodes = self._unique(query.captures(ast.root_node))
        sub_node_query = self._source_repository.tree_sitter_language.query(
            translate_to[self._source_repository.language][
                "nested_controlflow_subsequent_nodes"
            ]
        )
        for node, _ in inital_nodes:
            found = False
            nodes2 = sub_node_query.captures(node)
            for node2, _ in nodes2:
                if found:
                    break
                nodes3 = sub_node_query.captures(node2)
                for node3, _ in nodes3:
                    if found:
                        break
                    if len(sub_node_query.captures(node3)) > 0:
                        violations.append(
                            Violation(
                                "nested controlflow",
                                (
                                    str(file),
                                    node.start_point[0],
                                    node3.end_point[0] + 1,
                                ),
                            )
                        )
                        found = True
        return violations


metric = NestedControlflows()
