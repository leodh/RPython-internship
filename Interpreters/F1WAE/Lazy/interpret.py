import treeClass
import parser
 
def Interpret(tree, funDict, contVar):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and lazyness."""

    if isinstance(tree, treeClass.Num):
        return tree.n
    #
    elif isinstance(tree, treeClass.Op):
        left = Interpret(tree.lhs, funDict, contVar)
        right = Interpret(tree.rhs, funDict, contVar)
        if tree.op == '+':
            return left + right
        elif tree.op == '-':
            return left + right
        elif tree.op == '*':
            return left * right
        elif tree.op == '/':
            return left/right
        elif tree.op == '%':
            return left % right
        else:
            raise ValueError("Parsing Error, symobl "+ tree.op+" shouldn't be here.")
    #
    elif isinstance(tree, treeClass.With):
        newContVar = contVar.copy()
        newContVar[tree.name] = (tree.nameExpr, contVar) # Lazyness
        return Interpret(tree.body, funDict, newContVar)
    #
    elif isinstance(tree, treeClass.Id):
        try:
            expr, cont = contVar[tree.name]
            return Interpret(expr, funDict, cont) # Lazyness
        except KeyError:
            raise ValueError("Interpret Error: free identifier :\n" + tree.name)
    #
    elif isinstance(tree, treeClass.App):
        try:
            #
            funDef = funDict[tree.funName]
            if not isinstance(funDef, treeClass.Func):
                raise ValueError("Wrong Dictionnary.")
            newCont = {funDef.argName: (tree.arg, contVar)} # Lazyness
            return Interpret(funDef.body, funDict, newCont)
        #
        except KeyError:
            raise ValueError("Invalid function : " + tree.funName)
    #
    else: # Not an <F1WAE>
                raise ValueError("Argument of Interpret is not a <F1WAE>:\n")

def Main(file):
    t,d = parser.Parse(file)
    j = Interpret(t,d,{})
    print("the answer is :" + str(j))

if __name__ == "__main__":
    import sys
    try:
        with open(sys.argv[1],"r") as file:
                    prog = file.read()
        #print("The expression is:\n{}".format(expr))
                    Main(prog)
    except IndexError:
        print("You must supply a file to interpret")
