import treeClass
import parser
import sys

# So that you can still run this module under standard CPython, I add this
# import guard that creates a dummy class instead.
try:
    from pypy.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass

# JITing instructions
jitdriver = JitDriver(greens=['tree','funDict'], reds=['contVar'])

def Interpret(tree, funDict, contVar):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    jitdriver.jit_merge_point(tree=tree,funDict=funDict, contVar=contVar)

    if isinstance(tree, treeClass.Num):
        return tree.n
    #
    elif isinstance(tree, treeClass.Op):
        left = Interpret(tree.lhs, funDict, contVar)
        right = Interpret(tree.rhs, funDict, contVar)
        if tree.op == '+':
            return left + right
        elif tree.op == '-':
            return left - right
        elif tree.op == '*':
            return left * right
        elif tree.op == '/':
            return left/right
        elif tree.op == '%':
            return left % right
        elif tree.op == '=':
            if left == right:
                return 1
            else:
                return 0
        else:
            print("Parsing Error, symobl "+ tree.op+" shouldn't be here.")
            return 2
    #
    elif isinstance(tree, treeClass.With):
        val = Interpret(tree.nameExpr, funDict, contVar)
        contVar[tree.name] = val #Eager
        return Interpret(tree.body, funDict, contVar)
    #
    elif isinstance(tree, treeClass.Id):
        if tree.name in contVar.keys():
            return contVar[tree.name] 
        else:
            print("Interpret Error: free identifier :\n" + tree.name)
            return 2
    #
    elif isinstance(tree, treeClass.App):
        if tree.funName in funDict.keys():
            #
            funDef = funDict[tree.funName]
            val = Interpret(tree.arg, funDict, contVar)
            #
            if not isinstance(funDef, treeClass.Func):
                print("Wrong Dictionnary.")
            #
            newCont = {funDef.argName: val} # Eager
            return Interpret(funDef.body, funDict, newCont)
        #
        else:
            print("Invalid function : " + tree.funName)
            return 2
    #
    elif isinstance(tree, treeClass.If):
        condition = Interpret(tree.cond, funDict, contVar)
        if condition != 0: #True
            return Interpret(tree.ctrue, funDict, contVar)
        else:
            return Interpret(tree.cfalse, funDict, contVar)
    #
    else: # Not an <F1WAE>
        print("Argument of Interpret is not a <F1WAE>:\n")
        return 2  
        
def Main(file):
    t,d = parser.Parse(file)
    j = Interpret(t,d,{})
    print("the answer is :" + str(j))

import os

def jitpolicy(driver):
    from pypy.jit.codewriter.policy import JitPolicy
    return JitPolicy()

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
