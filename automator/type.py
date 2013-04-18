from ast import *

#=================================================================================
# Type Functions
#=================================================================================
def getType(node):
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

def getTypeName(type):
    return type['declname']

def getTypeString(type):
    s = type['type']
    for i in range(type['ptr_level']):
        s = s + '*'
    return s

def getTypeFormatString(type):
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
