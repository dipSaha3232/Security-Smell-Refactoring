import re
from urllib.parse import urlparse
import ast, astunparse
import string
import random


class EmptyPasswordRefactor(ast.NodeTransformer):
    def __init__(self):
        self.common_passwords = ['password','pass','pwd','passwd', 'upass']
    
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Tuple) and isinstance(node.value, ast.Tuple):
            index = 0
            for elt in node.targets[0].elts:
                name = elt.id
                if name is not None and isinstance(node.value.elts[index], ast.Constant):
                    value = node.value.elts[index].value
                    if isinstance(value, str) and (value is None or len(value) == 0) : 
                        for pwd in self.common_passwords:
                            if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), name.lower().strip())):
                                node.value.elts[index].value = str(''.join(random.choices(string.ascii_letters, k=10)))
            return node

        if isinstance(node.targets[0], ast.Attribute):
            if isinstance(node.targets[0].attr, str) :
                name = node.targets[0].attr

        elif isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id

        if name is not None and isinstance(node.value, ast.Constant) :
            value = node.value.value
            if isinstance(value, str) and (value is None or len(value) == 0) : 
                for pwd in self.common_passwords:
                    if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), name.lower().strip())):
                        node.value.value = str(''.join(random.choices(string.ascii_letters, k=10)))

        elif name is not None and isinstance(node.value, ast.Dict):
            pairs = zip(node.value.keys, node.value.values)
            index = 0
            for pair in pairs:
                key = pair[0].id
                if key is not None and isinstance(pair[1], ast.Constant) :
                    value = pair[1].value
                    if isinstance(value, str) and (value is None or len(value) == 0) :
                        for pwd in self.common_passwords:
                            if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), key.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), key.lower().strip())):
                                node.value.values[index].value = str(''.join(random.choices(string.ascii_letters, k=10)))
                index +=1


        self.generic_visit(node)
        return node

    def visit_keyword(self, node):
        arg = node.arg
        for pwd in self.common_passwords:
            if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), arg.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), arg.lower().strip())):
                        node.value.value = str(''.join(random.choices(string.ascii_letters, k=10)))
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        targetArgs = []
        if len(node.args.defaults) != 0 :
            targetArgs = node.args.args[-len(node.args.defaults):]
        index = 0
        for targetArg in targetArgs:
            name = targetArg.arg
            if name is not None and isinstance(node.args.defaults[index], ast.Constant):
                value = node.args.defaults[index].value
                if isinstance(value, str) and (value is None or len(value) == 0) :
                        for pwd in self.common_passwords:
                            if (re.match(r'[_A-Za-z0-9-\.]*{pwd}\b'.format(pwd = pwd), name.lower().strip()) or re.match(r'\b{pwd}[_A-Za-z0-9-\.]*'.format(pwd = pwd), name.lower().strip())):
                                node.args.defaults[index].value = str(''.join(random.choices(string.ascii_letters, k=10)))

            index += 1
        return node