from ast import List
from tree_sitter import Language, Parser


class SourceCart:
    def __init__(self):
        self.ast = ast
        self.language = Language("./build/my-languages.so", "python")
        self.parser = Parser()
        self.plugins = List()

    def getAST(self):
        pass

    def getLanguage(self):
        pass

    def getParser(self):
        pass

    def getSourceRoot(self):
        pass
