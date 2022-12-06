import re
from urllib.parse import urlparse
import ast, astunparse
from pprint import pprint

class CommandInjectionRefactor(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        
    def visit_keyword(self, node):
        if node.arg == "shell" and node.value.value == True :
            node.value.value = False
        self.generic_visit(node)
        return node
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if (node.func.value.id == 'subprocess' or node.func.value.id == 'os') and node.func.attr == 'Popen':
                if isinstance(node.args[0], ast.Name):
                    id = node.args[0].id
                    node.args[0] = ast.Call(func=ast.Attribute(value=ast.Name(id='shlex', ctx=ast.Load()), attr='strip', ctx=ast.Load()), 
                            args=[ast.Call(func=ast.Attribute(value=ast.Name(id='shlex', ctx=ast.Load()), attr='quote', ctx=ast.Load()),
                            args=[ast.Name(id=id, ctx=ast.Load())], keywords=[])], keywords=[])

                elif isinstance(node.args[0], ast.Constant):
                    value = str(node.args[0].value)
                    node.args[0] = ast.Call(func=ast.Attribute(value=ast.Name(id='shlex', ctx=ast.Load()), attr='strip', ctx=ast.Load()), 
                            args=[ast.Call(func=ast.Attribute(value=ast.Name(id='shlex', ctx=ast.Load()), attr='quote', ctx=ast.Load()),
                            args=[ast.Constant(value=value)], keywords=[])], keywords=[])

        self.generic_visit(node)
        return node

