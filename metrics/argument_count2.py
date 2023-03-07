from byoqm.plugin import PluginInterface
from byoqm.source_cart import SourceCart


class ArgumentCount(PluginInterface):
    def __init__(self, byoqm: SourceCart):
        self.src = byoqm.src_root
        self.language = byoqm.language
        self.parser = byoqm.parser
        # Initialize the metric with needed information.

    def run(self):
        # Run the metric and return the result.
        count = 0
        if self.src.is_file():
            with self.src.open() as f:
                count = self._parse(f)
        else:
            py_files = self.src.glob("**/*.py")
            for file in py_files:
                with open(file) as f:
                    count += self._parse(f)
            py_files.close()
        return count

    def _parse(self, file):
        count = 0
        tree = self.parser.parse(bytes(file.read(), "utf8"))
        query = self.language.query(
            """
            (function_definition
                parameters: (parameters) @function.parameters)
            """
        )
        captures = query.captures(tree.root_node)
        for node, _ in captures:
            if node.named_child_count > 4:
                count += 1

        return count
