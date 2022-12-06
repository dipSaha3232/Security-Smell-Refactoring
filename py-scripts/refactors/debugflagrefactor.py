import ast, astunparse
from pprint import pprint

class DebugFlagRefactor(ast.NodeTransformer):

    restricted_names = ['debug','debug_propagate_exceptions','propagate_exceptions']

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name is not None and (name.lower() in self.restricted_names or self.has_debug_in_name(name.lower())) :
                if isinstance(node.value, ast.Constant):
                    node.value = ast.parse('False').body[0].value

        elif isinstance(node.targets[0], ast.Attribute):
            if isinstance(node.targets[0].attr, str) :
                name = node.targets[0].attr
                if name is not None and (name.lower() in self.restricted_names or self.has_debug_in_name(name.lower())) :
                    if isinstance(node.value, ast.Constant):
                        node.value = ast.parse('False').body[0].value
        
        self.generic_visit(node)
        return node
    
    def visit_Expr(self, node):
        for keyword in node.value.keywords:
            if(keyword.arg is not None and isinstance(keyword.arg, str) and keyword.arg.lower() in self.restricted_names):
                keyword.value = ast.parse('False').body[0].value
        self.generic_visit(node)
        return node

    def has_debug_in_name(self, var_name):
        for name in self.restricted_names:
            if name in var_name.lower().strip(): 
                return True
        
        return False