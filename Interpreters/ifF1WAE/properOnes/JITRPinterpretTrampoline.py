import treeClass
import parser
import sys

# So that you can still run this module under standard CPython, I add this
# import guard that creates a dummy class instead.
# (from Pypy's tutorial by Andrew Brown)
try:
    from pypy.rlib.jit import JitDriver, purefunction
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass

@purefunction
def GetFunc(funDict, name):
    """Equivalent to funDict[name], but labelled as purefunction in JITing version to be run faster by the JITing VM.
    Used here to make comparison accurate."""

    body = funDict.get(name, treeClass.NoneFunc())
    if isinstance(body, treeClass.NoneFunc) :
        print("Inexistant function : "+ name)
    return body

##########################
# Class Function for CPS #
##########################
class Contk:
    def __init__(self):
        pass

class Endk(Contk):
    def __init__(self):
        pass

    def apply(self, arg):
        return NoMoreBounce(arg)

class Opk(Contk):
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
            return NoMoreBounce(2)

class OpLeftk(Contk):
    def __init__(self, exprRight, funDict, env, k, op):
        self.exprRight=exprRight
        self.funDict=funDict
        self.env=env
        self.k=k
        self.op=op

    def apply(self, arg):
        return ToBounce(self.exprRight, self.env, Opk(arg,self.op,self.k))

class Appk(Contk):
    def __init__(self, funName, funDict, k):
        self.funName=funName
        self.funDict=funDict
        self.k=k

    def apply(self, arg):
        g = GetFunc(self.funDict, self.funName)
        if not isinstance(g, treeClass.NoneFunc):
            return ToBounce(g.body, {g.argName: arg}, self.k)
        else:
            return NoMoreBounce(2)


class Ifk(Contk):
    def __init__(self, true, false, funDict, env, k):
        self.true=true
        self.false=false
        self.funDict=funDict
        self.env=env
        self.k=k

    def apply(self,arg):
        if arg != 0:
            return ToBounce(self.true, self.env, self.k)
        else:
            return ToBounce(self.false, self.env, self.k)

class Evalk(Contk):
    def __init__(self, body, name, env, k):
        self.body = body
        self.name = name
        self.env = env
        self.k = k

    def apply(self, arg):
        self.env[self.name] = arg
        return ToBounce(self.body, self.env, self.k)

##########
# Bounce #
##########

class Bounce:
    def __init__(self):
        pass

class ToBounce(Bounce):
    def __init__(self, expr, env, k):
        self.expr = expr
        self.env = env
        self.k = k

class NoMoreBounce(Bounce):
    def __init__(self,value):
        self.value = value

##############
# Trampoline #
##############

# JITing instructions


def get_printable_location(funDict, expr):
    return treeClass.treePrint(expr)

jitdriver = JitDriver(greens=['funDict', 'expr'], reds=['k','env'],
        get_printable_location=get_printable_location)

def Trampoline(expr, funDict, env, k):
    """ Interpret the ifF1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    bouncer = ToBounce(expr, env, k)
    expr = expr
    env = env
    k = k
    
    while 1:

        jitdriver.jit_merge_point(funDict, expr, k, env)
        if isinstance(bouncer, NoMoreBounce):
            break
        
        else:
            expr = bouncer.expr
            env = bouncer.env
            k = bouncer.k
            
            #
            if isinstance(expr, treeClass.Num):
                bouncer = k.apply(expr.n)
            #
            elif isinstance(expr, treeClass.Op):
                k2 = OpLeftk(expr.rhs, funDict, env, k, expr.op)
                bouncer = ToBounce(expr.lhs, env, k2)
            #
            elif isinstance(expr, treeClass.With):
                k2 = Evalk(expr.body, expr.name, env, k)
                bouncer = ToBounce(expr.nameExpr, env, k2)
            #
            elif isinstance(expr, treeClass.Id):
                try:
                    arg = env[expr.name]
                except KeyError:
                    print("Interpret Error: free identifier :\n" + expr.name)
                    arg = 2
                bouncer = k.apply(arg)
            #
            elif isinstance(expr, treeClass.App):
                bouncer = ToBounce(expr.arg, env, Appk(expr.funName, funDict, k))
                expr = bouncer.expr
                env = bouncer.env
                k = bouncer.k
                jitdriver.can_enter_jit(funDict, expr, env, k)
            #
            elif isinstance(expr, treeClass.If):
                bouncer = ToBounce(expr.cond, env, Ifk(expr.ctrue,expr.cfalse,funDict,env,k))
            #
            else: # Not an <ifF1WAE>
                print("Argument of Interpk is not a <ifF1WAE>:\n")
                bouncer = NoMoreBounce(2)
            #

    assert isinstance(bouncer, NoMoreBounce)
    return bouncer.value

#############################    
# Translation and execution #
#############################

def Main(file):
    t,d = parser.Parse(file)
    j = Trampoline(t,d,{},Endk())
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
