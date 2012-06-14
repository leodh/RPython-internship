import treeClass

def readItem(string):
    """Get the first following item (parenthesized block or integer). We consider there are no meaningless character (e.g. letters or spaces)"""

    count = 0
    cut = -1
    length = len(string)
    i = 0

    while i < length:
        if string[i] == '(':
            count +=1
        elif string[i] == ')':
            count -= 1
        else:
            pass
        
        if count == 0:
            cut = i
            break

        i += 1
        
    if cut == -1: 
        raise ValueError("Invalid (or empty) expression")
    else:
        l = len(string)
        return string[0:(i+1)], string[(i+1):l]

        
def parser(arithExpr):
    """Takes the arithmetic expression (without spaces) and turns it into a tree."""

    last = len(arithExpr) - 1
    if last > 0 :
        arith = arithExpr[1:last]
    else:
        arith = arithExpr

    head, tail = readItem(arith)
    if head in ('0','1','2','3','4','5','6','7','8','9'): 
        return treeClass.Leaf(int(head))
    elif head in ('+','-'): 
        ls , rs = readItem(tail) 
        return treeClass.InsideNode(head,parser(ls),parser(rs))
    else:
        raise ValueError("Invalid expression: " + head)




    
        
        
        
