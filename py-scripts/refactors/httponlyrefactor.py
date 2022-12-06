import re
from urllib.parse import urlparse
import ast, astunparse
from pprint import pprint

class HttpOnlyRefactor(ast.NodeTransformer):

    def __init__(self):
        self.http_libs = ['httplib.urlretrieve','urllib.request.urlopen','urllib.urlopen','urllib2.urlopen','requests.get', 
                        'requests.post','urllib.request.Request','httplib.HTTPConnection','httplib2.Http.request'
                    ]

        self.new_http_libs = ['urllib3.PoolManager.request']
    
    def visit_Constant(self, node):
        if node.value is not None and self.is_valid_http_url(node.value):
            node.value = self.convertHttpToHttps(node.value)
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        for keyword in node.keywords : 
            value = keyword.value.value
            if value is not None and self.is_valid_http_url(value):
                keyword.value.value = self.convertHttpToHttps(value)

        for arg in node.args:
            value = None
            if isinstance(arg, ast.Constant):
                value = arg.value
            if value is not None and self.is_valid_http_url(value):
                arg.value = self.convertHttpToHttps(value)
        self.generic_visit(node)
        return node

    def convertHttpToHttps(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme == 'http':
            parsed_url = parsed_url._replace(scheme = "https")
        return parsed_url.geturl()

    def is_valid_http_url(self, url): 

        reg_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(url))
        url = reg_url[0] if len(reg_url) > 0 else None
        if url is None: return False

        parsed_url = urlparse(url)

        if parsed_url.scheme == 'http': return True
        elif parsed_url.scheme == 'https': return False

        else: return True