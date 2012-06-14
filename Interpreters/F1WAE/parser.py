import treeClass

# Build associativity of braces


# To optmisize= calculate size of stack and dic beforehand
def BuildAssociativity(fileToUse):
    """ Build a associative table of braces. """

    # print(fileToUse)
    bracketMap = {}
    leftstack = []

    pc = 0
    # line = 1
    # indice = 1
    for char in fileToUse:
        if char in ('{', '}', '(',')'):
            # print(pc,line,indice, char)
            # print(pc, char)
            if char == '(' or char == '{':
                leftstack.append(pc)
            elif char == ')':
                # print(leftstack)
                left = leftstack.pop()
                # print("left =", left)
                # print(leftstack)
                if fileToUse[left] != '(':
                    raise ValueError("Should be } at " + str(pc)) # line "+str(line)+", character "+str(indice))
                right = pc
                bracketMap[left] = right
                bracketMap[right] = left
            elif char == '}':
                # print(leftstack)
                left = leftstack.pop()
                # print("left= ",left)
                # print(leftstack)
                if fileToUse[left] != '{':
                    raise ValueError("Should be ) at "+str(pc)) # line "+str(line)+", character "+str(indice))
                right = pc
                bracketMap[left] = right
                bracketMap[right] = left
            # elif char == '\n':
            #     print('hello')
            #     line +=1
            #     indice = 0
            else:
                pass
        else:
            pass
        pc += 1
        # indice += 1
            
    return bracketMap

## Test

# if __name__ == "__main__":
#     import sys
#     import os
#     try:
#         with open(sys.argv[1],"r") as fil:
#             print(BuildAssociativity(fil.read()))
#     except IndexError:
#         print('jesus')

        
# Spliting the original code into blocks

def FilterDic(dictry, start, end):
    """Return a new dictionnary containning only pairing of indices between start and (end-1) inclued."""

    def belong(n):
        return n<end and n>=start
    
    newDic ={}
    for i,k in dictry.items():
        if belong(i) and belong(k):
            newDic[i-start]=k-start
        elif belong(i) and not belong(k):
            raise ValueError("Not a valid bracket matching")
        else:
            pass
    # print("FilterDic :\n")
    # print(dictry, start, end)
    # print(newDic)
    return newDic

# def CutBlank(string, i):
#     """Find the first non-blank character following string[i] in string. If there's none, return the length of the list."""

#     if not (string[i] in (' ','\n','\t')):
#         return i
#     else:
#         try:
#             CutBlank(string,i+1)
#         except IndexError:
#             return i+1
    

def CutWord(string,i):
    """Find the first blank character following string[i] in string. If there's none, return the length of the list."""
    
    if string[i] in (' ','\n','\t'):
        return i
    else:
        try:
            return CutWord(string,i+1)
        except IndexError:
            return i+1
        

def SplittingCode(fileToUse, bracketMap):
    """ Splits the code into meaningful blocks. """

    # print("SplittingCode")
    # print(fileToUse)
    # print(bracketMap)
    pc = 0
    length = len(fileToUse)
    blocks = []
    
    while pc<length:
        ch = fileToUse[pc]
        if (ch in (' ', '\t', '\n')):
            pass
        elif ch =='(' or ch=='{':
            matchingBracket = bracketMap[pc] + 1
            block = fileToUse[pc:matchingBracket]
            # print(pc, matchingBracket, block)
            newDic = FilterDic(bracketMap, pc, matchingBracket)
            # print("done", length)
            blocks.append((block, newDic))
            pc = matchingBracket
        else:
            end = CutWord(fileToUse,pc)
            # print("end = " + str(end))
            blocks.append((fileToUse[pc:end], {}))
            # print("end = " + str(end))
            pc = end
        pc += 1
            
    return blocks

## Tests

# if __name__ == "__main__":
#     import sys
#     import os
#     try:
#         with open(sys.argv[1],"r") as fil:
#             d = BuildAssociativity(fil.read())
#             print('meuh')
#             print(SplittingCode(fil,d))
#     except IndexError:
#         print('lapin')


# Parsing function

def ParseFunc((block, dic)):
    """ Given a block defining a function, return the correspondant representation. There are only simple spaces. """

    n = dic[0]
    if not (block[0] == '{' and block[n] == '}'):
        raise ValueError("Not a function block :\n"+ block)
    else:
        workingBlock = block[1:n]
        # print(workingBlock)
        dic2 = FilterDic(dic,1,n)
        # print(dic2)
        subBlocks = SplittingCode(workingBlock, dic2)
        #
        if len(subBlocks) != 2:
            raise ValueError("Only two sub-blocks expected in block :\n"+block)
        else:
            declaration, dd = subBlocks[0]
            #
            if len(dd.values()) != 2 :
                raise ValueError("No sub-blocks expected inside of :\n" + declaration)
            #
            declareList = declaration[1:dd[0]].split(" ")
            if len(declareList) != 2:
                raise ValueError("Wrong declaration: \n" + declaration + "\nExpected form: <id> <id>")
            name = declareList[0]
            argName = declareList[1]
                
            bodyTree = ParseF1WAE(subBlocks[1])

    return name, treeClass.Func(name,argName,bodyTree)

def IsIdentifier(word):
    """True if word is a correct identifier"""
    
    def isAlphaOrUnd(c):
        return (c.replace('_','a')).isalpha()
    def isAlphaNumOrUnd(c):
        return (c.replace('_','a')).isalnum()
    return (isAlphaOrUnd(word[0]) and isAlphaNumOrUnd(word))


def ParseF1WAE((block, dic)):
    """Parses <F1WAE>. Only simple spaces."""

    # print(block)
    if block[0] == '{':
        raise ValueError("Function declaration is not allowed in <F1WAE> :\n" + block)
    #
    elif block[0] == '(':
        blockContent = (block[1:dic[0]]).strip()
        # print(blockContent)
        # First word in blockContent allows to identify the case
        head, space, tail = blockContent.partition(' ')
        #
        if head == 'with':
            # print(tail)
            bodyWith = SplittingCode(tail, FilterDic(dic,len(head+space)+1,dic[0]))
            if len(bodyWith) != 2:
                raise ValueError("Two expressions expected following keyword 'with':\n" + block)
            else:
                # print(bodyWith[0])
                falseApp = ParseF1WAE(bodyWith[0]) #Same syntax as an App
                if not(isinstance(falseApp, treeClass.App)):
                    raise ValueError("Wrong assignement in with block:\n" + block)
                else:
                    return treeClass.With(falseApp.funName, falseApp.arg, ParseF1WAE(bodyWith[1]))
            #
        elif head[0] in ('+','-','*','/','%'): # Treats the case were space is forgotten after operator
            bodyOp = SplittingCode((head[1:len(head)] + tail),FilterDic(dic,len(head+space)+1,dic[0]))
            if len(bodyOp) != 2:
                raise ValueError("Two expressions expected following operator :\n" + block)
            else:
                return treeClass.Op(head[0], ParseF1WAE(bodyOp[0]), ParseF1WAE(bodyOp[1]))
            #
        else: # An App or a parenthesized Num or Id
            bodyApp =  SplittingCode(tail, FilterDic(dic,len(head+space)+1,dic[0]))
            lenght = len(bodyApp)
            if lenght == 0: # Parenthesized Num or Id
                return ParseF1WAE((head, FilterDic(dic,1,dic[0])))
            elif lenght == 1: #An App
                return treeClass.App(head, ParseF1WAE(bodyApp[0]))
        #
    else:
        #
        if IsIdentifier(block):
            return treeClass.Id(block)
        elif block.isdigit():
            return treeClass.Num(int(block))
        else:
            raise ValueError("Syntax Error in identifier :\n" + block)

def Parse(myFile):
    """ The global parsing function. """
    
    myFile = (myFile.replace('\n',' ')).replace('\t',' ')
    # There are only simple spaces. Makes it easier to deal with.
    bracketMap = BuildAssociativity(myFile)
    codeInPieces = SplittingCode(myFile, bracketMap)
    #
    funcToDefine = []
    prog = []
    #
    for couple in codeInPieces:
        s,d = couple
        if s[0] == '{':
            funcToDefine.append((s,d))
        else:
            prog.append((s,d))
    #
    try: # Check that BNF is respected
        prog[1]
        raise ValueError("Only one <Prog> is allowed.")
    except IndexError:
        pass
    #
    # Create the function dictionnary
    funcDict = {}
    for funcDef in funcToDefine:
        name, descr = ParseFunc(funcDef)
        if not funcDict.has_key(name):
            funcDict[name] = descr
        else:
            raise ValueError("Function "+name+" already defined.")
    #
    # Create AST of main program
    ast = ParseF1WAE(prog[0])

    return ast, funcDict
    
    

##Tests

# if __name__ == "__main__":
#     import sys
#     import os
#     try:
#         with open(sys.argv[1],"r") as fil:
#             d = BuildAssociativity(fil.read())
#             print('meuh')
#             l=(SplittingCode(fil,d))
#             print('ninja')
#             li,di = l[0]
#             print(ParseFunc(li,di))
#     except IndexError:
#         print('omg, that\'s an atrocity')
    
