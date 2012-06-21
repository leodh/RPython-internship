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

##########################
# Class Function for CPS #
##########################

class Funck:
    def __init__(self):
        pass
    
    def apply(self,arg):
        return ExpVal(arg)

class Idk(Funck):
    def __init__(self):
        pass
    
    def apply(self,arg):
        return ExpVal(arg)

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
            print("Parsing Error, symobl "+ self.op +" shouldn't be here.")
            return ExpVal(2)

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
        if self.funName in self.funDict.keys():
            g=self.funDict[self.funName]
            return Interpk(g.body,self.funDict, {g.argName: arg}, self.k)
        else:
            print("Invalid function : " + self.funName)
            return ExpVal(2)

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


#####################
# Bounce Definition #
#####################

class Bounce:
    def __init__(self):
        pass

class ExpVal(Bounce):
    def __init__(self,val):
        self.val=val

class BounceFun(Bounce):
    def __init__(self,arg,funDict,env,funName,k):
        self.arg=arg
        self.funDict=funDict
        self.env=env
        self.funName=funName
        self.k=k
        
    def bounce(self):
        return Interpk(self.arg, self.funDict, self.env, Appk(self.funName, self.funDict, self.k))

def Trampoline(bouncer):
    """Execute the trampoline while there's still one to do"""
    
    if isinstance(bouncer,ExpVal):
        return bouncer.val
    elif isinstance(bouncer, BounceFun):
        return Trampoline(bouncer.bounce())
    else:
        print("Not a Bounce!")
        return 2

#############################    
#Interpret CPS - Trampoline #
#############################

# JITing instructions
jitdriver = JitDriver(greens=['tree','funDict'], reds=['env','k'])

def Interpk(tree, funDict, env,k):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    jitdriver.jit_merge_point(tree=tree, funDict=funDict, env=env, k=k)
    #
    if isinstance(tree, treeClass.Num):
        return k.apply(tree.n)
    #
    elif isinstance(tree, treeClass.Op):
        k2 = OpLeftk(tree.rhs, funDict, env, k, tree.op)
        return Interpk(tree.lhs, funDict, env, k2)
    #
    elif isinstance(tree, treeClass.With):
        
        val = Trampoline(Interpk(tree.nameExpr, funDict, env, Idk()))
        env[tree.name] = val #Eager
        return Interpk(tree.body, funDict, env, k)
    #
    elif isinstance(tree, treeClass.Id):
        if tree.name in env.keys():
            return k.apply(env[tree.name])
        else:
            print("Interpret Error: free identifier :\n" + tree.name)
            return k.apply(2)
    #
    elif isinstance(tree, treeClass.App):
        return BounceFun(tree.arg, funDict, env, tree.funName, k)
    #
    elif isinstance(tree, treeClass.If):
        return Interpk(tree.cond,funDict,env,Ifk(tree.ctrue,tree.cfalse,funDict,env,k))
    #
    else: # Not an <F1WAE>
        print("Argument of Interpk is not a <F1WAE>:\n")
        return k.apply(2)
    #


def Main(file):
    t,d = parser.Parse(file)
    bou = Interpk(t,d,{},Idk())
    j = Trampoline(bou)
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
