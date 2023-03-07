from ast import List
from pathlib import Path
from tree_sitter import Language, Parser


class SourceCart:
    def __init__(self, src_root: Path):
        self.language = Language("./build/my-languages.so", "python")
        self.parser = Parser()
        self.plugins = List()
        self.src_root = src_root

    def getAST(self):
        pass

    def getLanguage(self):
        pass

    def getParser(self):
        pass

    def getSourceRoot(self):
        pass
