import treeClass
import parser
import sys

from pypy.rlib.jit import JitDriver, elidable

##########################
# Class Function for CPS #
##########################
            
class Contk(object):
    def __init__(self,*arg):
        raise NotImplementedError("For abstract class")
    
    def apply(self,expr,env,val):
        raise NotImplementedError("For abstract class")


class Endk(Contk):
    def __init__(self,val):
        self.val = val

    def apply(self,expr, env, val):
        return expr, env, self, val

class Idk(Contk):
    def __init__(self):
        pass
    
    def apply(self, expr, env, val):
        return expr, env, Endk(val), val

class Withk(Contk):
    def __init__(self, expr, env, cont, name):
        self.expr = expr
        self.env = env
        self.cont = cont
        self.name = name

    def apply(self, expr, env, val):
        env2 = self.env
        env2[self.name]=val
        return self.expr, env2, self.cont, val

class Ifk(Contk):
    def __init__(self, env, cont, true, false):
        self.env = env
        self.cont = cont
        self.true = true
        self.false = false

    def apply(self, expr, env, val):
        if val:
            expAnsw = self.true
        else:
            expAnsw = self.false
        return expAnsw, self.env, self.cont, val

class Op1k(Contk):
    def __init__(self, env, cont, op, rhs):
        self.env = env
        self.cont = cont
        self.op = op
        self.rhs = rhs

    def apply(self, expr, env, val):
        cont = Op2k(self.cont, val, self.op)
        return self.rhs, self.env, cont, val

class Op2k(Contk):
    def __init__(self, cont, val, op):
        self.cont = cont
        self.val = val
        self.op = op

    def apply(self, expr, env, val):
        left = self.val
        right = val
        
        if self.op == '+':
            valAnsw = left + right
        elif self.op == '-':
            valAnsw = left - right
        elif self.op == '*':
            valAnsw = left * right
        elif self.op == '/':
            valAnsw = left / right
        elif self.op == '%':
            valAnsw = left % right
        elif self.op == '=':
            if left - right == 0:
                valAnsw = 1
            else:
                valAnsw = 0
        else:
            print("Parsing Error, symobl "+ self.op +" shouldn't be here.")
            valAnsw = 2
            
        return self.cont.apply(expr, env, valAnsw)

class Appk(Contk):
    def __init__(self, expr, cont, arg):
        self.expr = expr
        self.cont = cont
        self.arg = arg

    def apply(self, expr, env, val):
        return self.expr, {self.arg : val}, self.cont, val
        
##############################    
#Interpret Iterative, JITing #
##############################

@elidable
def GetFunc(funDict, name):
    """Equivalent to funDict[name], but labelled as elidable to be run faster by the JITing VM."""

    body = funDict.get(name, treeClass.NoneFunc())
    if isinstance(body, treeClass.NoneFunc):
        print("Inexistant function : "+ name)
    return body

def GetInEnv(env, name):
    """Equivalent to env[name]."""

    try:
        val = env[name]
    except KeyError:
        print("Interpret Error: free identifier :\n" + name)
        val = 2
    return val

# JITing instructions


def get_printable_location(funDict, expr):
    return treeClass.treePrint(expr)

jitdriver = JitDriver(greens=['funDict', 'expr'], reds=['val','cont','env'],
        get_printable_location=get_printable_location)

def Interpk(expr, funDict, env):
    """ Interpret the ifF1WAE AST given a set of defined functions. We use deferred substitution and eagerness."""

    val = -1
    funDict = funDict
    expr = expr
    env = env
    cont = Idk()

    while 1:
        #
        jitdriver.jit_merge_point(val=val, expr=expr, env=env, cont=cont, funDict=funDict)
        if isinstance(cont, Endk):
            break
        #
        if isinstance(expr, treeClass.Num):
            val = expr.n
            ex, en, co, va = cont.apply(expr,env,val) 
            expr = ex
            env = en
            cont = co
            val = va
        #
        elif isinstance(expr, treeClass.Id):
            val = GetInEnv(env, expr.name)
            ex, en, co, va = cont.apply(expr,env,val) 
            expr = ex
            env = en
            cont = co
            val = va
        #
        elif isinstance(expr, treeClass.With):
            cont = Withk(expr.body, env, cont, expr.name)
            expr = expr.nameExpr
        #
        elif isinstance(expr, treeClass.If):
            cont = Ifk(env, cont, expr.ctrue, expr.cfalse)
            expr = expr.cond
        #
        elif isinstance(expr, treeClass.Op):
            cont = Op1k(env, cont, expr.op, expr.rhs)
            expr = expr.lhs
        #
        elif isinstance(expr, treeClass.App):
            fun = GetFunc(funDict, expr.funName)
            if isinstance(fun, treeClass.NoneFunc):
                cont = Endk(2)
            else:
                body = fun.body
                arg = fun.argName
                expr = expr.arg
                cont = Appk(body, cont, arg)
                jitdriver.can_enter_jit(val=val, expr=expr, env=env, cont=cont, funDict=funDict)
        #
        else: # Not an <instr>
            print("Argument of Interpk is not a <instr>:\n")
            cont = Endk(2)
        # End of while
    assert isinstance(cont, Endk)
    return cont.val
    
def Main(file):
    t,d = parser.Parse(file)
    j = Interpk(t,d,{})
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
