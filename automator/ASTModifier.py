from pycparser import c_ast

import copy

from type import *
from util import getLocation

var = 0
vars = [{}]
funcs = {}

def addFunction(func):
    global funcs
    funcs[func['name']] = func

def getFunctions():
    global funcs
    return funcs

def enterFunction(funcname):
    global vars
    scope = copy.deepcopy(vars[-1])
    for param in funcs[funcname]['params']:
        scope[getTypeName(getType(param))] = param
    vars.append(scope)

def exitFunction(funcname):
    global vars
    vars.pop()

def enterScope():
    global vars
    vars.append(copy.deepcopy(vars[-1]))

def exitScope():
    global vars
    vars.pop()

def addVar(decl):
    global vars
    vars[-1][getTypeName(getType(decl))] = decl

def makeVarDecl(decl, init):
    global var
    newDecl = c_ast.Decl(
        '____' + str(var),
        decl.quals,
        decl.storage,
        decl.funcspec,
        copy.deepcopy(decl.type),
        init,
        decl.bitsize
    )
    node = newDecl.type
    while nodeType(node) == 'PtrDecl':
        node = node.type
    node.declname = '____' + str(var)
    var = var + 1
    return newDecl

def makeID(decl):
    return c_ast.ID(getTypeName(getType(decl)))

def makeFuncCallLog(func):
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:call({2})\\n"'.format(
                func['file'], func['line'], func['name']))
        ]))

def makeFuncReturnLog(coord, func, returnName = None):
    (file, line) = getLocation(coord)
    type = getType(func['type'])
    logString = '"{0}:{1}:return({2},{3},ret,'.format(
                file, line, func['name'], getTypeString(type))
    if returnName == None:
        logString = logString + 'undef)\\n"'
        return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', logString)
        ]))
    else:
        logString = logString + '{0})\\n"'.format(getTypeFormatString(type))
        return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', logString),
            c_ast.ID(returnName)
        ]))

def makeDeclLog(coord, declname):
    global vars
    type = getType(vars[-1][declname])
    (file, line) = getLocation(coord)
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:decl({2},{3})\\n"'.format(
                file, line, getTypeString(type), getTypeName(type)))
        ]))

def makeAssignLog(coord, declname, underlying = None):
    type = getType(vars[-1][declname])
    name = declname
    (file, line) = getLocation(coord)
    if underlying != None:
        name = underlying
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:assign({2},{3},{4})\\n"'.format(
                file, line, getTypeString(type),
                getTypeName(type), getTypeFormatString(type))),
            c_ast.ID(name)
        ]))

def makePostIncAssignLog(coord, declname, underlying = None):
    type = getType(vars[-1][declname])
    name = declname
    (file, line) = getLocation(coord)
    if underlying != None:
        name = underlying
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:assign({2},{3},{4})\\n"'.format(
                file, line, getTypeString(type),
                getTypeName(type), getTypeFormatString(type))),
            c_ast.BinaryOp('+', c_ast.ID(name), c_ast.Constant('int', '1'))
        ]))

def makePostDecAssignLog(coord, declname, underlying = None):
    type = getType(vars[-1][declname])
    name = declname
    (file, line) = getLocation(coord)
    if underlying != None:
        name = underlying
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:assign({2},{3},{4})\\n"'.format(
                file, line, getTypeString(type),
                getTypeName(type), getTypeFormatString(type))),
            c_ast.BinaryOp('-', c_ast.ID(name), c_ast.Constant('int', '1'))
        ]))

def makeScopeInLog(coord):
    (file, line) = getLocation(coord)
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:scope_in\\n"'.format(
            file, line))
        ]))

def makeScopeOutLog(coord):
    (file, line) = getLocation(coord)
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:scope_out\\n"'.format(
            file, line))
        ]))