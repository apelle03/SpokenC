from pycparser import c_ast

from ast import nodeType
from ASTModifier import *

def makeAssignExprLog(node):
    node = assignNode(node)
    node = makeAssignExpr(node)
    return node

def makeAssignExpr(node):
    if nodeType(node) == 'Assignment' and nodeType(node.lvalue) == 'ID':
        return c_ast.BinaryOp(
            '|',
            node,
            c_ast.BinaryOp(
                '==',
                makeAssignLog(node.coord, node.lvalue.name),
                c_ast.Constant('int', '0'),
                node.coord),
            node.coord)
    elif nodeType(node) == 'UnaryOp' and nodeType(node.expr) == 'ID':
        if node.op == 'p++':
            return c_ast.BinaryOp(
                '|',
                node,
                c_ast.BinaryOp(
                    '==',
                    makePostIncAssignLog(node.coord, node.expr.name),
                    c_ast.Constant('int', '0'),
                    node.coord),
                node.coord)
        elif node.op == 'p--':
            return c_ast.BinaryOp(
                '|',
                node,
                c_ast.BinaryOp(
                    '==',
                    makePostDecAssignLog(node.coord, node.expr.name),
                    c_ast.Constant('int', '0'),
                    node.coord),
                node.coord)
        elif node.op == '++' or node.op == '--':
            return c_ast.BinaryOp(
                '|',
                node,
                c_ast.BinaryOp(
                    '==',
                    makeAssignLog(node.coord, node.expr.name),
                    c_ast.Constant('int', '0'),
                    node.coord),
                node.coord)
    return node

def assignNode(node):
    if node == None:
        return None
    elif nodeType(node) == 'ArrayDecl':
        return assignArrayDecl(node)
    elif nodeType(node) == 'ArrayRef':
        return assignArrayRef(node)
    elif nodeType(node) == 'Assignment':
        return assignAssignment(node)
    elif nodeType(node) == 'BinaryOp':
        return assignBinaryOp(node)
    elif nodeType(node) == 'Break':
        return assignBreak(node)
    elif nodeType(node) == 'Case':
        return assignCase(node)
    elif nodeType(node) == 'Cast':
        return assignCast(node)
    elif nodeType(node) == 'Compound':
        return assignCompound(node)
    elif nodeType(node) == 'CompoundLiteral':
        return assignCompoundLiteral(node)
    elif nodeType(node) == 'Constant':
        return assignConstant(node)
    elif nodeType(node) == 'Continue':
        return assignContinue(node)
    elif nodeType(node) == 'Decl':
        return assignDecl(node)
    elif nodeType(node) == 'DeclList':
        return assignDeclList(node)
    elif nodeType(node) == 'Default':
        return assignDefault(node)
    elif nodeType(node) == 'DoWhile':
        return assignDoWhile(node)
    elif nodeType(node) == 'EllipsisParam':
        return assignEllipsisParam(node)
    elif nodeType(node) == 'EmptyStatement':
        return assignEmptyStatement(node)
    elif nodeType(node) == 'Enum':
        return assignEnum(node)
    elif nodeType(node) == 'Enumerator':
        return assignEnumerator(node)
    elif nodeType(node) == 'EnumeratorList':
        return assignEnumeratorList(node)
    elif nodeType(node) == 'ExprList':
        return assignExprList(node)
    elif nodeType(node) == 'FileAST':
        return assignFileAST(node)
    elif nodeType(node) == 'For':
        return assignFor(node)
    elif nodeType(node) == 'FuncCall':
        return assignFuncCall(node)
    elif nodeType(node) == 'FuncDecl':
        return assignFuncDecl(node)
    elif nodeType(node) == 'FuncDef':
        return assignFuncDef(node)
    elif nodeType(node) == 'Goto':
        return assignGoto(node)
    elif nodeType(node) == 'ID':
        return assignID(node)
    elif nodeType(node) == 'IdentifierType':
        return assignIdentifierType(node)
    elif nodeType(node) == 'If':
        return assignIf(node)
    elif nodeType(node) == 'Label':
        return assignLabel(node)
    elif nodeType(node) == 'NamedInitializer':
        return assignNamedInitializer(node)
    elif nodeType(node) == 'ParamList':
        return assignParamList(node)
    elif nodeType(node) == 'PtrDecl':
        return assignPtrDecl(node)
    elif nodeType(node) == 'Return':
        return assignReturn(node)
    elif nodeType(node) == 'Struct':
        return assignStruct(node)
    elif nodeType(node) == 'StructRef':
        return assignStructRef(node)
    elif nodeType(node) == 'Switch':
        return assignSwitch(node)
    elif nodeType(node) == 'TernaryOp':
        return assignTernaryOp(node)
    elif nodeType(node) == 'TypeDecl':
        return assignTypeDecl(node)
    elif nodeType(node) == 'Typedef':
        return assignTypedef(node)
    elif nodeType(node) == 'Typename':
        return assignTypename(node)
    elif nodeType(node) == 'UnaryOp':
        return assignUnaryOp(node)
    elif nodeType(node) == 'Union':
        return assignUnion(node)
    elif nodeType(node) == 'While':
        return assignWhile(node)
    else:
        print('===================================================================================')
        print('bad type' + nodeType)
        print('===================================================================================')
        return node

def assignArrayDecl(node):
    node.type = assignNode(node.type)
    node.dim = assignNode(node.dim)
    
    node.type = makeAssignExpr(node.type)
    node.dim = makeAssignExpr(node.dim)
    return node

def assignArrayRef(node):
    node.name = assignNode(node.name)
    node.subscript = assignNode(node.subscript)

    node.name = makeAssignExpr(node.name)
    node.subsrcipt = makeAssignExpr(node.subscript)
    return node

def assignAssignment(node):
    node.lvalue = assignNode(node.lvalue)
    node.rvalue = assignNode(node.rvalue)

    node.lvalue = makeAssignExpr(node.lvalue)
    node.rvalue = makeAssignExpr(node.rvalue)
    return node

def assignBinaryOp(node):
    node.left = assignNode(node.left)
    node.right = assignNode(node.right)

    node.left = makeAssignExpr(node.left)
    node.right = makeAssignExpr(node.right)
    return node

def assignBreak(node):
    return node

def assignCase(node):
    node.expr = assignNode(node.expr)
    for i in range(len(node.stmts)):
        node.stmts[i] = assignNode(node.stmts[i])

    node.expr = makeAssignExpr(node.expr)
    for i in range(len(node.stmts)):
        node.stmts[i] = makeAssignExpr(node.stmts[i])
    return node

def assignCast(node):
    node.to_type = assignNode(node.to_type)
    node.expr = assignNode(node.expr)

    node.to_type = makeAssignExpr(node.to_type)
    node.expr = makeAssignExpr(node.expr)
    return node

def assignCompound(node):
    for i in range(len(node.block_items)):
        node.block_items[i] = assignNode(node.block_items[i])
    for i in range(len(node.block_items)):
        node.block_items[i] = makeAssignExpr(node.block_items[i])
    return node

def assignCompoundLiteral(node):
    node.type = assignNode(node.type)
    node.init = assignNode(node.init)

    node.type = makeAssignExpr(node.type)
    node.init = makeAssignExpr(node.init)
    return node

def assignConstant(node):
    return node

def assignContinue(node):
    return node

def assignDecl(node):
    node.type = assignNode(node.type)
    node.init = assignNode(node.init)
    node.bitsize = assignNode(node.bitsize)

    node.type = makeAssignExpr(node.type)
    node.init = makeAssignExpr(node.init)
    node.bitsize = makeAssignExpr(node.bitsize)
    return node

def assignDeclList(node):
    for i in range(len(node.decls)):
        node.decls[i] = assignNode(node.decls[i])
    for i in range(len(node.decls)):
        node.decls[i] = makeAssignExpr(node.decls[i])
    return node

def assignDefault(node):
    for i in range(len(node.stmts)):
        node.stmts[i] = assignNode(node.stmts[i])
    for i in range(len(node.stmts)):
        node.stmts[i] = makeAssignExpr(node.stmts[i])
    return node

def assignDoWhile(node):
    node.cond = assignNode(node.cond)
    node.stmt = assignNode(node.stmt)

    node.cond = makeAssignExpr(node.cond)
    node.stmt = makeAssignExpr(node.stmt)
    return node

def assignEllipsisParam(node):
    return node

def assignEmptyStatement(node):
    return node

def assignEnum(node):
    node.values = assignNode(node.values)

    node.value = makeAssignExpr(node.value)
    return node

def assignEnumerator(node):
    node.value = assignNode(node.value)

    node.value = makeAssignExpr(node.value)
    return node

def assignEnumeratorList(node):
    for i in range(len(node.enumerators)):
        node.enumerators[i] = assignNode(node.enumerators[i])
    for i in range(len(node.enumerators)):
        node.enumerators[i] = makeAssignExpr(node.enumerators[i])
    return node

def assignExprList(node):
    for i in range(len(node.exprs)):
        node.exprs[i] = assignNode(node.exprs[i])
    for i in range(len(node.exprs)):
        node.exprs[i] = makeAssignExpr(node.exprs[i])
    return node

def assignFileAST(node):
    for i in range(len(node.ext)):
        node.ext[i] = assignNode(node.ext[i])
    for i in range(len(node.ext)):
        node.ext[i] = makeAssignExpr(node.ext[i])
    return node

def assignFor(node):
    node.init = assignNode(node.init)
    node.cond = assignNode(node.cond)
    node.next = assignNode(node.next)
    node.stmt = assignNode(node.stmt)

    node.init = makeAssignExpr(node.init)
    node.cond = makeAssignExpr(node.cond)
    node.next = makeAssignExpr(node.next)
    node.stmt = makeAssignExpr(node.stmt)
    return node

def assignFuncCall(node):
    node.name = assignNode(node.name)
    node.args = assignNode(node.args)

    node.name = makeAssignExpr(node.name)
    node.args = makeAssignExpr(node.args)
    return node

def assignFuncDecl(node):
    node.args = assignNode(node.args)
    node.type = assignNode(node.type)

    node.args = makeAssignExpr(node.args)
    node.type = makeAssignExpr(node.type)
    return node

def assignFuncDef(node):
    node.decl = assignNode(node.decl)
    node.body = assignNode(node.body)
    for i in range(len(node.param_decls)):
        node.param_decls[i] = assignNode(node.param_decls[i])

    node.decl = makeAssignExpr(node.decl)
    node.body = makeAssignExpr(node.body)
    for i in range(len(node.param_decls)):
        node.param_decls[i] = makeAssignExpr(node.param_decls[i])
    return node

def assignGoto(node):
    return node

def assignID(node):
    return node

def assignIdentifierType(node):
    return node

def assignIf(node):
    node.cond = assignNode(node.cond)
    node.iftrue = assignNode(node.iftrue)
    node.iffalse = assignNode(node,iffalse)

    node.cond = makeAssignExpr(node.cond)
    node.iftrue = makeAssignExpr(node.iftrue)
    node.iffalse = makeAssignExpr(node.iffalse)
    return node

def assignLabel(node):
    node.stmt = assignNode(node.stmt)

    node.stmt = makeAssignExpr(node.stmt)
    return node

def assignNamedInitializer(node):
    node.expr = assignNode(node.expr)
    for i in range(len(node.name)):
        node.name[i] = assignNode(node.name[i])

    node.expr = makeAssignExpr(node.expr)
    for i in range(len(node.name)):
        node.name[i] = makeAssignExpr(node.name[i])
    return node

def assignParamList(node):
    for i in range(len(node.params)):
        node.params[i] = assignNode(node.params[i])
    for i in range(len(node.params)):
        node.params[i] = makeAssignExpr(node.params[i])
    return node

def assignPtrDecl(node):
    node.type = assignNode(node.type)

    node.type = makeAssignExpr(node.type)
    return node

def assignReturn(node):
    node.expr = assignNode(node.expr)

    node.expr = makeAssignExpr(node.expr)
    return node

def assignStruct(node):
    for i in range(len(node.decls)):
        node.decls[i] = assignNode(node.decls[i])
    for i in range(len(node.decls)):
        node.decls[i] = makeAssignExpr(node.decls[i])
    return node

def assignStructRef(node):
    node.name = assignNode(node.name)
    node.field = assignNode(node.field)

    node.name = makeAssignExpr(node.name)
    node.field = makeAssignExpr(node.field)
    return node

def assignSwitch(node):
    node.cond = assignNode(node.cond)
    node.stmt = assignNode(node.stmt)

    node.cond = makeAssignExpr(node.cond)
    node.stmt = makeAssignExpr(node.stmt)
    return node

def assignTernaryOp(node):
    node.cond = assignNode(node.cond)
    node.iftrue = assignNode(node.iftrue)
    node.iffalse = assignNode(node.iffalse)

    node.cond = makeAssignExpr(node.cond)
    node.iftrue = makeAssignExpr(node.iftrue)
    node.iffalse = makeAssignExpr(node.iffalse)
    return node

def assignTypeDecl(node):
    node.type = assignNode(node.type)

    node.type = makeAssignExpr(node.type)
    return node

def assignTypedef(node):
    node.type = assignNode(node.type)

    node.type = makeAssignExpr(node.type)
    return node

def assignTypename(node):
    node.type = assignNode(node.type)

    node.type = makeAssignExpr(node.type)
    return node

def assignUnaryOp(node):
    node.expr = assignNode(node.expr)

    node.expr = makeAssignExpr(node.expr)
    return node

def assignUnion(node):
    for i in range(len(node.decls)):
        node.decls[i] = assignNode(node.decls[i])
    for i in range(len(node.decls)):
        node.decls[i] = makeAssignExpr(node.decls[i])
    return node

def assignWhile(node):
    node.cond = assignNode(node.cond)
    node.stmt = assignNode(node.stmt)

    node.cond = makeAssignExpr(node.cond)
    node.stmt = makeAssignExpr(node.stmt)
    return node
