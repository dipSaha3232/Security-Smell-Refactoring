import ast
from pprint import pprint

class AssertStatRefactor(ast.NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Assert(self, node):
        return None
