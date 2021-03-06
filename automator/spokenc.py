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
    return c_ast.Decl(
        node.decl.name,
        node.decl.quals,
        node.decl.storage,
        node.decl.funcspec,
        node.decl.type.type,
        None,
        node.decl.bitsize,
        node.decl.coord)
    #return node.decl.type;

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
        start = srcText.find('\n', start) + 1
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
    if nodeType(child.init) == 'DeclList':
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
    else:
        child.init = makeAssignExprLog(child.init)
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

#=================================================================================
# Unified Add Scope Dependent Debug Functions
#=================================================================================
def addDeclDebug(parent, child):
    name = getTypeName(getType(child))
    ASTModifier.addVar(child)
    index = [x[1] for x in parent.children()].index(child)
    parent.block_items = parent.block_items[:index + 1] + \
        [ASTModifier.makeDeclLog(child.coord, name)] + \
        [ASTModifier.makeAssignLog(child.coord, name)] + \
        parent.block_items[index + 1:]

def addAssignDebug(parent, child):
    name = child.lvalue.name
    index = [x[1] for x in parent.children()].index(child)
    parent.block_items = parent.block_items[:index + 1] + \
        [ASTModifier.makeAssignLog(child.coord, name)] + \
        parent.block_items[index + 1:]

def addUnopDebug(parent, child):
    name = child.expr.name
    index = [x[1] for x in parent.children()].index(child)
    parent.block_items = parent.block_items[:index + 1] + \
        [ASTModifier.makeAssignLog(child.coord, name)] + \
        parent.block_items[index + 1:]

def addScopeDependentDebug(node):
    for (name, child) in node.children():
        if nodeType(child) == 'For':
            ASTModifier.enterScope()
            addForDebug(node, child, [x[1] for x in node.children()].index(child))
            addScopeDependentDebug(child)
            ASTModifier.exitScope()
        elif nodeType(child) == 'While':
            ASTModifier.enterScope()
            addWhileDebug(node, child, [x[1] for x in node.children()].index(child))
            addScopeDependentDebug(child)
            ASTModifier.exitScope()
        elif nodeType(child) == 'DoWhile':
            ASTModifier.enterScope()
            addWhileDebug(node, child, [x[1] for x in node.children()].index(child))
            addScopeDependentDebug(child)
            ASTModifier.exitScope()
        elif nodeType(child) == 'If':
            ASTModifier.enterScope()
            addIfDebug(node, child, [x[1] for x in node.children()].index(child))
            addScopeDependentDebug(child)
            ASTModifier.exitScope()
        elif nodeType(node) == 'Compound' and nodeType(child) == 'Decl':
            addDeclDebug(node, child)
            addScopeDependentDebug(child)
        elif nodeType(node) == 'Compound' and nodeType(child) == 'Assignment' and nodeType(child.lvalue) == 'ID':
            addAssignDebug(node, child)
            addScopeDependentDebug(child)
        elif nodeType(node) == 'Compound' and (nodeType(child) == 'UnaryOp' and nodeType(child.expr) == 'ID' and
                (child.op == 'p++' or child.op == '++' or
                 child.op == 'p--' or child.op == '--')):
            addUnopDebug(node, child)
            addScopeDependentDebug(child)
        else:
            addScopeDependentDebug(child)
        

#=================================================================================
# Add Scope Break Debug Functions
#=================================================================================
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
    debug = [ASTModifier.makeFuncCallLog(func)]
    for param in func['params']:
        debug.append(ASTModifier.makeDeclLog(param.coord, getTypeName(getType(param))))
        debug.append(ASTModifier.makeAssignLog(param.coord, getTypeName(getType(param))))

    if func['body'].block_items != None:
        func['body'].block_items = debug + \
            func['body'].block_items + \
            [ASTModifier.makeFuncReturnLog(func['file'] + ':' + str(func['endLine']), func)]
    else:
        func['body'].block_items = debug + \
            [ASTModifier.makeFuncReturnLog(func['file'] + ':' + str(func['endLine']), func)]

def addFuncReturnDebug(func, node = None):
    if node == None:
        addFuncReturnDebug(func, func['body'])
    else:
        for (name, child) in node.children():
            if nodeType(child) == 'Return':                
                newDecl = ASTModifier.makeVarDecl(func['type'], child.expr)
                ASTModifier.addVar(newDecl)
                child.expr = ASTModifier.makeID(newDecl)
                
                index = [x[1] for x in node.children()].index(child)
                node.block_items = node.block_items[:index] + \
                    [newDecl] + \
                    [ASTModifier.makeFuncReturnLog(child.coord, func, getTypeName(getType(newDecl)))] + \
                    node.block_items[index:]
            elif child != None:
                addFuncReturnDebug(func, child)

#=================================================================================
# Main Transform Functions
#=================================================================================
def transformFunction(func):
    addScopeDependentDebug(func['body'])
    addScopeBreakDebug(func['body'])
    addFuncParamDebug(func)
    addFuncReturnDebug(func)
    return generator.visit(func['body'])

def main_process(filename = None):
    #print("================================================================")
    ast = getAst(filename)
    #print("================================================================")
    srcText = '';
    with open(filename) as infile:
        srcText = srcText + infile.read()
    #print("================================================================")
    for (i, topLevelDecl) in ast.children():
        if nodeType(topLevelDecl) == 'FuncDef':
            func = {'name' : getFunctionName(topLevelDecl),
                    'type' : getFunctionReturnType(topLevelDecl),
                    'params' : getFunctionParamlist(topLevelDecl),
                    'body' : getFunctionBody(topLevelDecl),
                    'file' : str(topLevelDecl.coord).split(':')[0],
                    'line' : int(str(topLevelDecl.coord).split(':')[1]) }
            endPos = getClosingSymbolLocation('{', '}', srcText, getFunctionLocation(srcText, func)[0])
            func['endLine'] = srcText.count('\n', 0, endPos) + 1
            ASTModifier.addFunction(func)
    #pp.pprint(ASTModifier.getFunctions())
    #print("================================================================")
    funcTexts = []
    for (name, func) in ASTModifier.getFunctions().iteritems():
        #print(func['name'])
        ASTModifier.enterFunction(name)
        funcTexts.append({'loc' : getFunctionLocation(srcText, func),
                          'text' : transformFunction(func)})
        ASTModifier.exitFunction(name)
        #print("================================================================")
    funcTexts = sorted(funcTexts, key=lambda k: k['loc'][0])
    newText = '#include <stdio.h>\n'
    last = 0
    for funcText in funcTexts:
        newText = newText + srcText[last:funcText['loc'][0]] + funcText['text']
        last = funcText['loc'][1] + 1
    newText = newText + srcText[last:]
    with open(filename + "-dbg.c", "w") as outfile:
        outfile.write(newText)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # TODO check if file exists
        main_process( filename = sys.argv[1])
    else:
        print("Please provide a filename as argument")
