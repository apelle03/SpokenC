from pycparser import c_ast

from type import *
from util import getLocation

var = 0
vars = {}
funcs = {}

def addFunction(func):
    global funcs
    funcs[func['name']] = func

def getFunctions():
    global funcs
    return funcs

def enterFunction(funcname):
    global vars
    for param in funcs[funcname]['params']:
        vars[getTypeName(getType(param))] = param

def exitFunction(funcname):
    global vars
    vars = {}

def addVar(decl):
    global vars
    vars[getTypeName(getType(decl))] = decl

def makeVarDecl(decl, init):
    global var
    decl = c_ast.Decl(
        '____' + str(var),
        decl.quals,
        decl.storage,
        decl.funcspec,
        c_ast.TypeDecl(
            '____' + str(var),
            decl.type.quals,
            decl.type.type),
        init,
        decl.bitsize
    )
    var = var + 1
    return decl

def makeID(decl):
    return c_ast.ID(getTypeName(getType(decl)))

def makeDeclLog(coord, declname):
    global vars
    type = getType(vars[declname])
    (file, line) = getLocation(coord)
    return c_ast.FuncCall(
        c_ast.ID('fprintf'),
        c_ast.ExprList([
            c_ast.ID('stderr'),
            c_ast.Constant('string', '"{0}:{1}:decl({2},{3})\\n"'.format(
                file, line, getTypeString(type), getTypeName(type)))
        ]))

def makeAssignLog(coord, declname, underlying = None):
    type = getType(vars[declname])
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
    type = getType(vars[declname])
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
    type = getType(vars[declname])
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