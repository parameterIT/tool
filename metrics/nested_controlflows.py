from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class NestedControlflows(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._parse(self._source_repository.get_ast(file_info), file_info)
                )
        return Result("nested controlflow", violations, len(violations))

    def _unique(self, not_unique_list):
        unique_list = []

        for x in not_unique_list:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    def _parse(self, ast, file_info):
        """
        Finds the control statements of a file and returns the amount of control statements that have a nested
        control flow depth of at least 4
        """
        violations = []
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        query_str = translate_to[file_info.language]["method_control_flow"]
        if file_info.language == "python" or file_info.language == "c_sharp":
            query_str += translate_to[file_info.language]["global_control_flow"]
        if file_info.language == "java" or file_info.language == "c_sharp":
            query_str += translate_to[file_info.language]["constructor_control_flow"]
        query = tree_sitter_language.query(query_str)
        inital_nodes = self._unique(query.captures(ast.root_node))
        sub_node_query = tree_sitter_language.query(
            translate_to[file_info.language]["nested_controlflow_subsequent_nodes"]
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
                    nodes4 = sub_node_query.captures(node3)
                    for node4, _ in nodes4:
                        if found:
                            break
                        if len(sub_node_query.captures(node4)) > 0:
                            violations.append(
                                Violation(
                                    "nested controlflow",
                                    (
                                        str(file_info.file_path),
                                        node.start_point[0],
                                        node4.end_point[0] + 1,
                                    ),
                                )
                            )
                            found = True
        return violations


metric = NestedControlflows()
