from refactors.debugflagrefactor import DebugFlagRefactor
from refactors.emptypasswordrefactor import EmptyPasswordRefactor
from refactors.httponlyrefactor import HttpOnlyRefactor
from refactors.assertstatrefactor import AssertStatRefactor
from refactors.commandinjectionrefactor import CommandInjectionRefactor
from refactors.xssrefactor import XSSRefactor

import ast, astunparse, sys

class RefactorEngine():
    
    def __init__(self, source_code):
        self.source_code = source_code
    
    def refactorCode(self):
        parse = ast.parse(self.source_code)
        # print(ast.dump(parse))

        emptyPasswordRefactor = EmptyPasswordRefactor()
        httpOnlyRefactor = HttpOnlyRefactor()
        debugFlagRefactor = DebugFlagRefactor()
        assertStatRefactor = AssertStatRefactor()
        commandInjectionRefactor = CommandInjectionRefactor()
        xssRefactor = XSSRefactor()

        emptyPasswordRefactor.visit(parse)
        httpOnlyRefactor.visit(parse)
        debugFlagRefactor.visit(parse)
        assertStatRefactor.visit(parse)
        commandInjectionRefactor.visit(parse)
        xssRefactor.visit(parse)

        sys.stdout.write(astunparse.unparse(parse))
        # print(astunparse.unparse(parse))
