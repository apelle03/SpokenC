#=================================================================================
# Utility Functions
#=================================================================================
def getClosingSymbolLocation(open, close, src, pos):
    if src.find(open, pos) == pos:
        opens = 1
        while opens > 0:
            pos = pos + 1
            if src[pos] == open:
                opens = opens + 1
            elif src[pos] == close:
                opens = opens - 1
        return pos
    else:
        return None

def getClosingSymbolLine(open, close, src, pos):
    pos = getClosingSymbolLocation(open, close, src, pos)
    if pos != None:
        src.count('\n', 0, pos) + 1
    else:
        return None

def getLocation(coord):
    file = str(coord).split(':')[0]
    line = int(str(coord).split(':')[1])
    return (file, line)
