import treeClass
import parser
import sys

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
        
        
######################    
#Interpret Iterative #
######################


def Interpk(tree, funDict, env1):
    """ Interpret the ifF1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    expr = tree
    env = env1
    cont = Idk()
    val = -1

    #value-of/k
    while not(isinstance(cont,Endk)):

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
            if expr.name in env.keys():
                val = (env[expr.name])
            else:
                print("Interpret Error: free identifier :\n" + tree.name)
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
            if not expr.funName in funDict.keys():
                print("Inexistant function : "+expr.funName)
            fun = funDict[expr.funName]
            body = fun.body
            arg = fun.argName
            expr = expr.arg
            cont = Appk(body, cont, arg)
        #
        else: # Not an <ifF1WAE>
            print("Argument of Interpk is not a <ifF1WAE>:\n")
            cont = Endk(2)
        # End of while
    assert isinstance(cont, Endk)
    return cont.val

#############################    
# Translation and execution #
#############################

def Main(file):
    t,d = parser.Parse(file)
    j = Interpk(t,d,{})
    print("the answer is :" + str(j))

import os

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
