from __future__ import print_function
import sys
import pprint
import re

sys.path.extend(['.', '..'])

from pycparser import parse_file, c_parser, c_generator
from pycparser import c_ast

pp = pprint.PrettyPrinter( indent = 4 )
funcs = {}
vars = {}
var = 0

def is_FuncDef(node):
    return node.__class__.__name__ == "FuncDef"

def is_TypeDecl(node):
    return node.__class__.__name__ == "TypeDecl"

def is_PtrDecl(node):
    return node.__class__.__name__ == "PtrDecl"

def nodeType(node):
    return node.__class__.__name__;

def get_ast(filename):
    global pp
    ast = parse_file(filename,
                     use_cpp = True,
                     cpp_path = '/usr/bin/cpp',
                     cpp_args = [ r'-I./utils/fake_libc_include' ], )
    ast.show(showcoord = False)
    return ast

def get_type(node):
    typeInfo = {};
    typeInfo['ptr_level'] = 0
    node = node.type
    while nodeType(node) == "PtrDecl":
        typeInfo['ptr_level'] = typeInfo['ptr_level'] + 1
        node = node.type
    typeInfo['declname'] = node.declname
    typeInfo['type'] = node.type.names[0]
    for type in node.type.names[1:]:
        typeInfo['type'] = typeInfo['type'] + ' ' + type
    return typeInfo;

def get_function_name(node):
    assert(is_FuncDef(node))
    return node.decl.name;

def get_function_return_type(node):
    assert(is_FuncDef(node))
    return get_type(node.decl.type);

def get_function_paramlist(node):
    assert(is_FuncDef(node))
    paramlist = []
    if node.decl.type.args != None:
        for param in node.decl.type.args.params:
            paramlist.append(get_type(param))
    return paramlist

def get_function_body(node):
    assert(is_FuncDef(node))
    return node.body;

def get_type_string(type):
    s = type['type']
    for i in range(type['ptr_level']):
        s = s + '*'
    return s

def get_format_for_type(type):
    if type['ptr_level'] > 0:
        if type['ptr_level'] == 1 and type['type'] == 'char':
            return '%s'
        else:
            return '%p'
    elif type['type'].find('float') != -1 or type['type'].find('double') != -1:
        return '%f'
    elif type['type'].find('char') != -1:
        return '%c'
    elif type['type'].find('unsigned') != -1:
        s = '%'
        for i in range(type['type'].count('long')):
            s = s + 'l'
        for i in range(type['type'].count('short')):
            s = s + 'h'
        return s + 'u'
    elif type['type'].find('int') != -1:
        s = '%'
        for i in range(type['type'].count('long')):
            s = s + 'l'
        for i in range(type['type'].count('short')):
            s = s + 'h'
        return s + 'd'
    return '%p'

def get_closing_symbol_location(open, close, src, (line, char)):
    if src[line].find(open, char) == char:
        opens = 1
        while opens > 0:
            char = char + 1
            while char >= len(src[line]):
                line = line + 1
                char = 0
                if line >= len(src):
                    return None
            if src[line][char] == open:
                opens = opens + 1
            elif src[line][char] == close:
                opens = opens - 1
        return (line, char)
    else:
        return None

def add_func_decl_debug(src, func):
    pp.pprint(func)
    lineNum = int(func['line'])
    # call
    while src[lineNum].find('{') == -1:
        lineNum = lineNum + 1
    callLog = 'fprintf(stderr, "{0}:{1}:call({2})\\n");\n'.format(
        func['file'], func['line'], func['name'])

    # args
    for arg in func['params']:
        callLog = callLog + 'fprintf(stderr, "{0}:{1}:decl({2},{3})\\n");\n'.format(
            func['file'], func['line'],
            get_type_string(arg), arg['declname'])
        callLog = callLog + 'fprintf(stderr, "{0}:{1}:assign({2},{3},{4})\\n", {5});\n'.format(
            func['file'], func['line'],
            get_type_string(arg), arg['declname'], get_format_for_type(arg),
            arg['declname'])
    src[lineNum] = src[lineNum].replace('{', '{\n' + callLog)
    
    # return
    (line, char) = get_closing_symbol_location('{', '}',
                    src, (lineNum, src[lineNum].find('{')))
    returnLog = 'fprintf(stderr, "{0}:{1}:return({2},{3},{4},{5})\\n");\n'.format(
        func['file'], func['line'], func['name'],
        get_type_string(func['type']), 'ret', 'undef')
    src[line] = src[line][:char] + returnLog + src[line][char:]

def add_func_body_debug(src, func):
    for (name, child) in func['body'].children():
        add_node_debug(src, child)

def add_node_debug(src, node):
    recur = True
    if nodeType(node) == 'Decl':
        add_decl_debug(src, node)
    elif nodeType(node) == 'Assignment':
        add_assign_debug(src, node)
    elif nodeType(node) == 'For':
        add_for_debug(src, node)
        recur = False
    if recur:
        for (name, child) in node.children():
            add_node_debug(src, child)

def add_decl_debug(src, node):
    file = str(node.coord).split(':')[0]
    ln = int(str(node.coord).split(':')[1])
    type = get_type(node)
    vars[node.name] = type
    declName = re.compile('[^a-zA-Z0-9_]' + node.name + '[^a-zA-Z0-9_]')

    line = ln
    match = declName.search(src[line])
    while match == None:
        line = line + 1
        match = declName.search(src[line])
    start = match.start() + 1
    semi = -1
    while semi == -1:
        semi = src[line].find(';', start)
        if semi == -1:
            start = 0
            line = line + 1
    declLog = '\nfprintf(stderr, "{0}:{1}:decl({2},{3})\\n");'.format(
        file, ln, get_type_string(type), node.name)
    if node.init != None:
        declLog = declLog + '\nfprintf(stderr, "{0}:{1}:assign({2},{3},{4})\\n", {5});'.format(
            file, ln, get_type_string(type), node.name,
            get_format_for_type(type), node.name)
    src[line] = src[line][:semi + 1] + declLog + src[line][semi + 1:]

def add_assign_debug(src, node):
    print('assign')
    file = str(node.coord).split(':')[0]
    ln = int(str(node.coord).split(':')[1])
    if nodeType(node.lvalue) == 'ID':
        type = vars[node.lvalue.name]
        print(get_type_string(vars[node.lvalue.name]))

        declName = re.compile('[^a-zA-Z0-9_]' + node.lvalue.name + '[^a-zA-Z0-9_]')
        # find lvalue position
        line = ln
        match = declName.search(src[line])
        while match == None:
            line = line + 1
            match = declName.search(src[line])
        # find equal sign position
        start = match.start() + 1
        eq = -1
        while eq == -1:
            eq = src[line].find('=', start)
            if eq == -1:
                start = 0
                line = line + 1
        # find semicolon position
        start = eq
        semi = -1
        while semi == -1:
            semi = src[line].find(';', start)
            if semi == -1:
                start = 0
                line = line + 1
        
        assignLog = '\nfprintf(stderr, "{0}:{1}:assign({2},{3},{4})\\n", {5});'.format(
            file, ln, get_type_string(type), node.lvalue.name,
            get_format_for_type(type), node.lvalue.name)
        src[line] = src[line][:semi + 1] + assignLog + src[line][semi + 1:]
        print(assignLog)

def add_for_debug(src, node):
    file = str(node.coord).split(':')[0]
    ln = int(str(node.coord).split(':')[1])

    decls = []
    if node.init != None:
        for (name, child) in node.init.children():
            decls.append(get_type(child))
    beforeLog = ''
    ################################f
    generator = c_generator.CGenerator()
    ################################f
    global var
    startVar = var
    i = 0
    for decl in decls:
        if node.init.decls[i].init != None:
            beforeLog = beforeLog + '{0} ____{1} = {2};\n'.format(
                get_type_string(decl), var, generator.visit(node.init.decls[i].init))
        else:
            beforeLog = beforeLog + '{0} ____{1};\n'.format(
                get_type_string(decl), var)
        var = var + 1
        i = i + 1
    beforeLog = beforeLog + 'fprintf(stderr, "{0}:{1}:scope_in\\n");\n'.format(
        file, ln)
    global pp
    pp.pprint(decls)
    forLog = 'for ('
    i = 0
    for decl in decls:
        beforeLog = beforeLog + 'fprintf(stderr, "{0}:{1}:decl({2},{3})\\n");\n'.format(
            file, ln, get_type_string(decl), decl['declname'])
        beforeLog = beforeLog + 'fprintf(stderr, "{0}:{1}:assign({2},{3},{4})\\n", ____{5});\n'.format(
            file, ln, get_type_string(decl), decl['declname'], get_format_for_type(decl), startVar)
        node.init.decls[i].init = c_ast.ID('____' + str(startVar), None)
        startVar = startVar + 1
        i = i + 1
    forLog = forLog + generator.visit(node.init) + '; ' + generator.visit(node.cond) + '; ' + generator.visit(node.next) + ') '
    print(forLog)
    match = re.search('[^a-zA-Z0-9_]for[^a-zA-Z0-9_]', src[ln])
    src[ln] = src[ln][:match.start() + 1] + beforeLog + src[ln][match.start() + 1:]
    
    line = ln
    brace = src[line].find('{')
    while brace == -1:
        line = line + 1
        brace = src[line].find('{')
    updateLog = ''
    for decl in decls:
        updateLog = updateLog + '\nfprintf(stderr, "{0}:{1}:assign({2},{3},{4})\\n", {5});'.format(
        file, ln, get_type_string(decl), decl['declname'],
        get_format_for_type(decl), decl['declname'])
    src[line] = src[line][:brace + 1] + updateLog + src[line][brace + 1:]
    (line, brace) = get_closing_symbol_location('{', '}', src, (line, brace))
    afterLog = 'fprintf(stderr, "{0}:{1}:scope_out\\n");\n'.format(
        file, line)
    src[line] = src[line][:brace + 1] + afterLog + src[line][brace + 1:]

def split_returns(src, node, func):
    if nodeType(node) == 'Return':
        split_return(src, node, func)
    for (name, child) in node.children():
        split_returns(src, child, func)

def split_return(src, node, func):
    global var
    if node.expr == None:
        return
    line = int(str(node.coord).split(':')[1])
    returnLoc = src[line].find('return ')
    exprLoc = returnLoc + 7
    endLoc = src[line].find(';')
    newReturn = get_type_string(func['type']) + ' ____' + str(var) + ' = ' + src[line][exprLoc:endLoc] + ';\n'
    newReturn = newReturn + 'fprintf(stderr, "{0}:{1}:return({2},{3},ret,{4})\\n", ____{5});\n'.format(
        func['file'], func['line'],
        func['name'], get_type_string(func['type']),
        get_format_for_type(func['type']), str(var))
    newReturn = newReturn + 'return ____' + str(var)
    var = var + 1
    src[line] = src[line][:returnLoc] + newReturn + src[line][endLoc:]

def add_func_names(func):
    for param in func['params']:
        vars[param['declname']] = param

def remove_func_names(func):
    vars = {}
    #for param in func['params']:
    #    del vars[param['declname']]

def main_process(filename = None):
    global pp
    global funcs
    global vars
    print("================================================================")
    ast = get_ast(filename)
    print("================================================================")
    topLevelDecls = ast.children()
    for (i, topLevelDecl) in topLevelDecls:
        #pp.pprint(topLevelDecl)
        if is_FuncDef(topLevelDecl):
            func = {'name' : get_function_name(topLevelDecl),
                    'type' : get_function_return_type(topLevelDecl),
                    'params' : get_function_paramlist(topLevelDecl),
                    'body' : get_function_body(topLevelDecl),
                    'file' : str(topLevelDecl.coord).split(':')[0],
                    'line' : str(topLevelDecl.coord).split(':')[1] }
            funcs[func['name']] = func
    pp.pprint(funcs)
    print("================================================================")
    lines = ['#include <stdio.h>'];
    with open(filename) as infile:
        srcText = infile.read().splitlines()
    for line in srcText:
        lines.append(line)
    for (name, func) in funcs.iteritems():
        split_returns(lines, func['body'], func)
    print("================================================================")
    for name, func in funcs.iteritems():
        add_func_names(func)
        add_func_decl_debug(lines, func)
        add_func_body_debug(lines, func)
        remove_func_names(func)
        print("================================================================")

    with open(filename + "-dbg.c", "w") as outfile:
        for line in lines:
            outfile.write(line)
            outfile.write('\n')

#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # TODO check if file exists
        main_process( filename = sys.argv[1])
    else:
        print("Please provide a filename as argument")
