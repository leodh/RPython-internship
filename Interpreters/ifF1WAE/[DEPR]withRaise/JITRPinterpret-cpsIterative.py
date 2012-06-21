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

#Class Function for CPS

class Funck:
    def __init__(self):
        pass
    
    def apply(self,arg):
        return arg

class Idk(Funck):
    def __init__(self):
        pass
    
    def apply(self,arg):
        return arg

class Opk(Funck):
    def __init__(self,argLeft,op,k):
        self.argLeft=argLeft
        self.op=op
        self.k=k


    def apply(self,arg):
        if self.op == '+':
            return self.k.apply(self.argLeft + arg)
        elif self.op == '-':
            return self.k.apply(self.argLeft - arg)
        elif self.op == '*':
            return self.k.apply(self.argLeft * arg)
        elif self.op == '/':
            return self.k.apply(self.argLeft / arg)
        elif self.op == '%':
            return self.k.apply(self.argLeft % arg)
        elif self.op == '=':
            if self.argLeft - arg == 0:
                return self.k.apply(1)
            else:
                return self.k.apply(0)
        else:
            raise ValueError("Parsing Error, symobl "+ self.op +" shouldn't be here.")

class OpLeftk(Funck):
    def __init__(self, exprRight, funDict, env, k, op):
        self.exprRight=exprRight
        self.funDict=funDict
        self.env=env
        self.k=k
        self.op=op

    def apply(self, arg):
        return Interpk(self.exprRight,self.funDict,self.env, Opk(arg,self.op,self.k))

class Appk(Funck):
    def __init__(self, funName, funDict, k):
        self.funName=funName
        self.funDict=funDict
        self.k=k

    def apply(self, arg):
        try:
            g=self.funDict[self.funName]
        except KeyError:
            raise ValueError("Invalid function : " + self.funName)
        return Interpk(g.body,self.funDict, {g.argName: arg}, self.k)

class Ifk(Funck):
    def __init__(self, true, false, funDict, env, k):
        self.true=true
        self.false=false
        self.funDict=funDict
        self.env=env
        self.k=k

    def apply(self,arg):
        if arg != 0:
            return Interpk(self.true, self.funDict, self.env, self.k)
        else:
            return Interpk(self.false, self.funDict, self.env, self.k)


# JITing instructions
jitdriver = JitDriver(greens=['tree','funDict','env','k'], reds=[])

#Interpret CPS - tail recursive


def Interpk(tree, funDict, env,k):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    jitdriver.jit_merge_point(tree=tree, funDict=funDict, env=env,k=k)
    
    if isinstance(tree, treeClass.Num):
        return k.apply(tree.n)
    #
    elif isinstance(tree, treeClass.Op):
        k2 = OpLeftk(tree.rhs, funDict, env, k, tree.op)
        return Interpk(tree.lhs, funDict, env, k2)
    #
    elif isinstance(tree, treeClass.With):
        val = Interpk(tree.nameExpr, funDict, env, Idk())
        env[tree.name] = val #Eager
        return Interpk(tree.body, funDict, env, k)
    #
    elif isinstance(tree, treeClass.Id):
        try:
            return k.apply(env[tree.name])
        except KeyError:
            raise ValueError("Interpret Error: free identifier :\n" + tree.name)
    #
    elif isinstance(tree, treeClass.App):
        return Interpk(tree.arg, funDict, env, Appk(tree.funName, funDict, k))
    #
    elif isinstance(tree, treeClass.If):
        return Interpk(tree.cond,funDict,env,Ifk(tree.ctrue,tree.cfalse,funDict,env,k))
    #
    else: # Not an <F1WAE>
        raise ValueError("Argument of Interpk is not a <F1WAE>:\n")

def Main(file):
    t,d = parser.Parse(file)
    j = Interpk(t,d,{},Idk())
    print("the answer is :" + str(j))

import os

def jitpolicy(driver):
    from pypy.jit.codewriter.policy import JitPolicy
    return JitPolicy()

def run(fp):
    program_envents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_envents += read
    os.close(fp)
    Main(program_envents)

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
