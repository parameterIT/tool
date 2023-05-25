from core.metric.metric import Metric
from core.metric.result import Result
from core.metric.violation import Violation
from core.source_repository.source_repository import SourceRepository
from metrics.util.language_util import translate_to, SUPPORTED_LANGUAGES


class MethodCount(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self):
        violations = []
        for _, file_info in self._source_repository.files.items():
            if file_info.language in SUPPORTED_LANGUAGES:
                violations.extend(
                    self._parse(self._source_repository.get_ast(file_info), file_info)
                )
        return Result("method count", violations, len(violations))

    def _parse(self, ast, file_info):
        """
        Finds the amount of methods for a file, and returns whether or not the method count is greater than 20
        """
        violations = []
        tree_sitter_language = self._source_repository.tree_sitter_languages[
            file_info.language
        ]
        function_block = translate_to[file_info.language]["function"]
        class_definition = translate_to[file_info.language]["class"]
        if not file_info.language == "python":
            function_block += translate_to[file_info.language]["constructor"]
        class_query = tree_sitter_language.query(
            f"""
            ({class_definition}) @class
            """
        )
        classes = class_query.captures(ast.root_node)
        query = tree_sitter_language.query(
            f"""
            (_ [{function_block}] @function)
            """
        )
        
        if len(classes) < 1:
            captures = query.captures(ast.root_node)
            violation = self._save_violations(captures, file_info)
            if violation != None:
                violations.append(violation)
        else:
            for c in classes:
                captures = query.captures(c[0])
                violation = self._save_violations(captures, file_info)
                if violation != None:
                    violations.append(violation)
        return violations
        
    def _save_violations(self, captures, file_info):
        if len(captures) > 20:
            return Violation(
                    "method count",
                    (
                        str(file_info.file_path),
                        captures[0][0].start_point[0] + 1,
                        captures[len(captures) - 1][0].end_point[0],
                    ),
                )
        else: 
            return None
            

metric = MethodCount()
