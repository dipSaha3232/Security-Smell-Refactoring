import json

from filters.assertstat import AssertStatement
from filters.xss import Xss
from filters.debugflag import DebugFlag
from filters.httponly import HttpWithoutTLS
from filters.emptypassword import EmptyPassword
from filters.commandinjection import CommandInjection

class RuleEngine():
    
    def __init__(self, tokens, src_file_name):
        self.tokens = tokens
        self.src_file_name = src_file_name


    def filter(self):

        try:
            imported_modules = self.get_imported_modules()
            
            assert_statement = AssertStatement()
            debug_flag = DebugFlag()
            xss = Xss()
            empty_password = EmptyPassword()
            http_without_tls = HttpWithoutTLS()
            command_injection = CommandInjection()

        except Exception as error:
            print(error)


        for token in self.tokens:
            try:
                token = json.loads(token)
                # print(token)
                
                assert_statement.detect_smell(token, self.src_file_name)
                xss.detect_smell(token, self.src_file_name)
                debug_flag.detect_smell(token, self.src_file_name)
                empty_password.detect_smell(token, self.src_file_name)
                http_without_tls.detect_smell(token, self.src_file_name)
                command_injection.detect_smell(token, self.src_file_name)

            except Exception as error: 
                print(json.dumps("Error detecting tokens"))
            

    def get_imported_modules(self):

        imported_modules = []
        for token in self.tokens:
            try: 
                token = json.loads(token)
                if token['type'] == 'import':
                    imported_modules.append(token['og'])

            except Exception as error: print(str(error))
        return imported_modules
