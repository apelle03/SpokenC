from __future__ import print_function
import sys
import pprint
import re

sys.path.extend(['.', '..'])

from pycparser import parse_file, c_parser, c_generator
from pycparser import c_ast

import ASTModifier

from ast import *
from type import *
from util import *

from assignments import makeAssignExprLog

pp = pprint.PrettyPrinter( indent = 4 )
generator = c_generator.CGenerator()

#=================================================================================
# Function Functions
#=================================================================================
def getFunctionName(node):
    assert(nodeType(node) == 'FuncDef')
    return node.decl.name;

def getFunctionReturnType(node):
    assert(nodeType(node) == 'FuncDef')
    return node.decl.type;

def getFunctionParamlist(node):
    assert(nodeType(node) == 'FuncDef')
    paramlist = []
    if node.decl.type.args != None:
        for param in node.decl.type.args.params:
            paramlist.append(param)
    return paramlist

def getFunctionBody(node):
    assert(nodeType(node) == 'FuncDef')
    return node.body;

def getFunctionLocation(srcText, func):
    start = 0
    for i in range(func['line'] - 1):
        start = srcText.find('\n', start)
    start = srcText.find('{', start)
    finish = getClosingSymbolLocation('{', '}', srcText, start)
    return (start, finish)

#=================================================================================
# Add Scope Debug Functions
#=================================================================================
def addForDebug(parent, child, index):
    if nodeType(parent) != 'Compound':
        return
    preFor = [ASTModifier.makeScopeInLog(child.coord)]
    postFor = [ASTModifier.makeScopeOutLog(child.coord)]
    for (name, decl) in child.init.children():
        newDecl = ASTModifier.makeVarDecl(decl, decl.init)
        ASTModifier.addVar(decl)
        ASTModifier.addVar(newDecl)
        preFor.append(newDecl)
        preFor.append(ASTModifier.makeDeclLog(child.coord,
                                              getTypeName(getType(decl))))
        preFor.append(ASTModifier.makeAssignLog(child.coord,
                                                getTypeName(getType(decl)),
                                                getTypeName(getType(newDecl))))
        decl.init = ASTModifier.makeID(newDecl)
    child.cond = makeAssignExprLog(child.cond)
    child.next = makeAssignExprLog(child.next)
        
    parent.block_items = parent.block_items[:index] + \
                         preFor + \
                         [parent.block_items[index]] + \
                         postFor + \
                         parent.block_items[index + 1:]

def addWhileDebug(parent, child, index):
    if nodeType(parent) != 'Compound':
        return
    child.cond = makeAssignExprLog(child.cond)
    parent.block_items = parent.block_items[:index] + \
                         [ASTModifier.makeScopeInLog(child.coord)] + \
                         [parent.block_items[index]] + \
                         [ASTModifier.makeScopeOutLog(child.coord)] + \
                         parent.block_items[index + 1:]

def addIfDebug(parent, child, index):
    if nodeType(child.iftrue) == 'Compound':
        if child.iftrue.block_items == None:
            child.iftrue.block_items = [
                ASTModifier.makeScopeInLog(child.coord),
                ASTModifier.makeScopeOutLog(child.coord)]
        else:
            child.iftrue.block_items = [ASTModifier.makeScopeInLog(child.coord)] + \
                child.iftrue.block_items + \
                [ASTModifier.makeScopeOutLog(child.coord)]
    if nodeType(child.iffalse) == 'Compound':
        if child.iffalse.block_items == None:
            child.iffalse.block_items = [
                ASTModifier.makeScopeInLog(child.coord),
                ASTModifier.makeScopeOutLog(child.coord)]
        else:
            child.iffalse.block_items = [ASTModifier.makeScopeInLog(child.coord)] + \
                child.iffalse.block_items + \
                [ASTModifier.makeScopeOutLog(child.coord)]

def addScopeDebug(node):
    for (name, child) in node.children():
        if nodeType(child) == 'For':
            addForDebug(node, child, [x[1] for x in node.children()].index(child))
        elif nodeType(child) == 'While':
            addWhileDebug(node, child, [x[1] for x in node.children()].index(child))
        elif nodeType(child) == 'DoWhile':
            addWhileDebug(node, child, [x[1] for x in node.children()].index(child))
        elif nodeType(child) == 'If':
            addIfDebug(node, child, [x[1] for x in node.children()].index(child))
        addScopeDebug(child)

def addBreakDebug(parent, index, debugs):
    if nodeType(parent) != 'Compound':
        return
    debugs.reverse()
    parent.block_items = parent.block_items[:index] + \
                         debugs + \
                         parent.block_items[index:]
    debugs.reverse()

def addScopeBreakDebug(node, outs = []):
    if node == None:
        return
    if nodeType(node) == 'If':
        outs[-1].pop()
        outs[-1].append(ASTModifier.makeScopeOutLog(node.coord))
        addScopeBreakDebug(node.iftrue, outs)
        addScopeBreakDebug(node.iffalse, outs)
    else:
        for (name, child) in node.children():
            if child == None:
                return
            elif (nodeType(child) == 'For' or
                nodeType(child) == 'While' or
                nodeType(child) == 'DoWhile'):
                    outs.append([ASTModifier.makeScopeOutLog(child.coord)])
                    addScopeBreakDebug(child.stmt, outs)
                    outs.pop()
            elif nodeType(child) == 'If':
                if len(outs) == 0:
                    outs.append([])
                outs[-1].append(ASTModifier.makeScopeOutLog(child.coord))
                addScopeBreakDebug(child.iftrue, outs)
                addScopeBreakDebug(child.iffalse, outs)
                outs[-1].pop()
            elif nodeType(child) == 'Break':
                addBreakDebug(node, [x[1] for x in node.children()].index(child), outs[-1])
            else:
                addScopeBreakDebug(child, outs)

#=================================================================================
# Add Function Debug Functions
#=================================================================================
def addFuncParamDebug(func):
    pass

def addFuncReturnDebug(func):
    pass

#=================================================================================
# Add Variable Debug Functions
#=================================================================================
def addVarDeclDebug(node):
    if nodeType(node) != 'Compound':
        for (name, child) in node.children():
            addVarDeclDebug(child)
    else:
        for (name, child) in node.children():
            if nodeType(child) == 'Decl':
                name = getTypeName(getType(child))
                ASTModifier.addVar(child)
                index = [x[1] for x in node.children()].index(child)
                node.block_items = node.block_items[:index + 1] + \
                    [ASTModifier.makeDeclLog(child.coord, name)] + \
                    [ASTModifier.makeAssignLog(child.coord, name)] + \
                    node.block_items[index + 1:]
            addVarDeclDebug(child)

def addVarAssignDebug(node):
    if nodeType(node) != 'Compound':
        for (name, child) in node.children():
            addVarAssignDebug(child)
    else:
        for (name, child) in node.children():
            if nodeType(child) == 'Assignment' and nodeType(child.lvalue) == 'ID':
                name = child.lvalue.name
                index = [x[1] for x in node.children()].index(child)
                node.block_items = node.block_items[:index + 1] + \
                    [ASTModifier.makeAssignLog(child.coord, name)] + \
                    node.block_items[index + 1:]
            elif (nodeType(child) == 'UnaryOp' and nodeType(child.expr) == 'ID' and
                (child.op == 'p++' or child.op == '++' or
                 child.op == 'p--' or child.op == '--')):
                    name = child.expr.name
                    index = [x[1] for x in node.children()].index(child)
                    node.block_items = node.block_items[:index + 1] + \
                        [ASTModifier.makeAssignLog(child.coord, name)] + \
                        node.block_items[index + 1:]
            addVarAssignDebug(child)

#=================================================================================
# Main Transform Functions
#=================================================================================
def transformFunction(srcText, func):
    addVarDeclDebug(func['body'])
    addVarAssignDebug(func['body'])
    addScopeDebug(func['body'])
    addScopeBreakDebug(func['body'])
    addFuncParamDebug(func)
    addFuncReturnDebug(func)
    (first, last) = getFunctionLocation(srcText, func)
    return srcText[:first] + generator.visit(func['body']) + srcText[last + 1:]

def main_process(filename = None):
    print("================================================================")
    ast = getAst(filename)
    print("================================================================")
    for (i, topLevelDecl) in ast.children():
        if nodeType(topLevelDecl) == 'FuncDef':
            func = {'name' : getFunctionName(topLevelDecl),
                    'type' : getFunctionReturnType(topLevelDecl),
                    'params' : getFunctionParamlist(topLevelDecl),
                    'body' : getFunctionBody(topLevelDecl),
                    'file' : str(topLevelDecl.coord).split(':')[0],
                    'line' : int(str(topLevelDecl.coord).split(':')[1]) }
            ASTModifier.addFunction(func)
    pp.pprint(ASTModifier.getFunctions())
    print("================================================================")
    srcText = '#include <stdio.h>\n';
    with open(filename) as infile:
        srcText = srcText + infile.read()
    print("================================================================")
    for (name, func) in ASTModifier.getFunctions().iteritems():
        ASTModifier.enterFunction(name)
        srcText = transformFunction(srcText, func)
        ASTModifier.exitFunction(name)
        print("================================================================")

    with open(filename + "-dbg.c", "w") as outfile:
        outfile.write(srcText)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # TODO check if file exists
        main_process( filename = sys.argv[1])
    else:
        print("Please provide a filename as argument")
