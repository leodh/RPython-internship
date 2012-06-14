import RPtreeClass
import RPparser
import sys #Necessary only to use the file in the Pypy interpreter all along TTC annotations

def Substitute(expr, var, val):
    """Handle substitution of var by value val in expr. """

    if isinstance(expr, RPtreeClass.Num):
        return expr
    #
    elif isinstance(expr, RPtreeClass.Op):
        newLhs = Substitute(expr.lhs, var, val)
        newRhs = Substitute(expr.rhs, var, val)
        return RPtreeClass.Op(expr.op, newLhs, newRhs)
    #
    elif isinstance(expr, RPtreeClass.With):
        newNameExpr = Substitute(expr.nameExpr, var, val)
        if expr.name == var:
            return RPtreeClass.With(expr.name, newNameExpr, expr.body)
        else:
            newBody = Substitute(expr.body, var, val)
            return RPtreeClass.With(expr.name, newNameExpr, newBody)
    #
    elif isinstance(expr, RPtreeClass.Id):
        if expr.name == var:
            return val
        else:
            return expr
    #   
    elif isinstance(expr, RPtreeClass.App):
        newArg = Substitute(expr.arg, var, val)
        return RPtreeClass.App(expr.funName, newArg)
    #
    else: # Not an F1WAE expression
            raise ValueError("Argument of Substitute is not a <F1WAE>:\n" + expr)
 
def Interpret(tree, funDict, contVar):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and lazyness."""

    if isinstance(tree, RPtreeClass.Num):
        return tree.n
    #
    elif isinstance(tree, RPtreeClass.Op):
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
    elif isinstance(tree, RPtreeClass.With):
        newContVar = contVar.copy()
        newContVar[tree.name] = (tree.nameExpr, contVar) # Lazyness
        return Interpret(tree.body, funDict, newContVar)
    #
    elif isinstance(tree, RPtreeClass.Id):
        try:
            expr, cont = contVar[tree.name]
            return Interpret(expr, funDict, cont) # Lazyness
        except KeyError:
            raise ValueError("Interpret Error: free identifier :\n" + tree.name)
    #
    elif isinstance(tree, RPtreeClass.App):
        try:
            #
            funDef = funDict[tree.funName]
            if not isinstance(funDef, RPtreeClass.Func):
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
    t,d = RPparser.Parse(file)
    j = Interpret(t,d,{})
    print("The answer is :" + str(j))

import os

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    Main(program_contents)

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    run(os.open(filename, os.O_RDONLY, 0777))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
