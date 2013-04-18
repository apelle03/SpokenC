from pycparser import parse_file

#=================================================================================
# AST Functions
#=================================================================================
def nodeType(node):
    if node == None:
        return None
    return node.__class__.__name__;

def getAst(filename):
    global pp
    ast = parse_file(filename,
                    use_cpp = True,
                    cpp_path = '/usr/bin/cpp',
                    cpp_args = [ r'-I./utils/fake_libc_include' ], )
    #ast.show(showcoord = True)
    return ast
