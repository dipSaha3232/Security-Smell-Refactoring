import ast
from engine import RuleEngine

class XSSRefactor(ast.NodeTransformer):
    module_list = []

    def __init__(self):
        super().__init__()

    # def visit_alias(self, node):
    #     self.module_list.append(node.name)

    # def add_import_statement(self):
    #     import_modules = RuleEngine.get_imported_modules()
    #     if 'flask.jsonify' not in import_modules and 'jsonify' not in import_modules:


    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) :
            if node.func.id == 'render_template_string' :
                node.func.id = 'render_template'
        self.generic_visit(node)
        return node
    
    def operateOnReturnNode(self, node):
        for n in ast.iter_child_nodes(node):
            if isinstance(n,ast.Return):
                if isinstance(n.value,ast.Call) and isinstance(n.value.func, ast.Name):
                    if n.value.func.id != 'jsonify':
                        n.value = ast.Call(func=ast.Name(id='jsonify', ctx=ast.Load()), args=[n.value],keywords=[])
                else :
                    n.value = ast.Call(func=ast.Name(id='jsonify', ctx=ast.Load()), args=[n.value],keywords=[])
            self.operateOnReturnNode(n)

    def visit_FunctionDef(self, node):
        needJsonify = False
        for decorator in node.decorator_list :
            if self.isRoutingCall(decorator):
                needJsonify = True
                break
        if needJsonify:
            self.operateOnReturnNode(node)

        self.generic_visit(node)
        return node

    # def visit_Module(self, node):
    #     import_modules = RuleEngine.get_imported_modules()
    #     if 'flask.jsonify' not in import_modules and 'jsonify' not in import_modules:
    #         node.body.insert(0,ast.Import(names=[ast.alias(name='flask.jsonify')]))

    def isRoutingCall(self, node):
        if isinstance(node.func, ast.Attribute): 
            if node.func.value.id == 'app' and node.func.attr == 'route':
                return True
        
        return False