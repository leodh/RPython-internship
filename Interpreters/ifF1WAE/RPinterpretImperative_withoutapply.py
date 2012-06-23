import treeClass
import parser
import sys


#Class Function for CPS

## I have to use these four functions because I get return a tuple containing a Contk (ttc)

class Contk:
    def __init__(self):
        raise NotImplementedError("For abstract class")
    
    def newExpr(self, expr, env, val):
        return expr
        # raise NotImplementedError("For abstract class")

    def newEnv(self, expr, env, val):
        return env
        # raise NotImplementedError("For abstract class")

    def newCont(self, expr, env, val):
        return self
        # raise NotImplementedError("For abstract class")

    def newVal(self, expr, env, val):
        return val
        # raise NotImplementedError("For abstract class")


class Endk(Contk):
    def __init__(self,val):
        self.val = val

    def newExpr(self, expr, env, val):
        print("Illicit call to Endk.newExpr")
        return expr

    def newEnv(self, expr, env, val):
        print("Illicit call to Endk.newEnv")
        return env

    def newCont(self, expr, env, val):
        print("Illicit call to Endk.newCont")
        return Endk(2)

    def newVal(self, expr, env, val):
        return self.val

class Idk(Contk):
    def __init__(self):
        pass

    def newExpr(self, expr, env, val):
        return expr

    def newEnv(self, expr, env, val):
        return env

    def newCont(self, expr, env, val):
        assert isinstance(val, int)
        return Endk(val)

    def newVal(self, expr, env, val):
        return val

class Withk(Contk):
    def __init__(self, expr, env, cont, val, name, body):
        self.expr = expr
        self.env = env
        self.cont = cont
        self.val = val
        self.name = name
        self.body = body

    def newExpr(self, expr, env, val):
        return self.body

    def newEnv(self, expr, env, val):
        env2 = self.env
        env2[self.name]=val
        return env2

    def newCont(self, expr, env, val):
        return self.cont

    def newVal(self, expr, env, val):
        return val

class Ifk(Contk):
    def __init__(self, expr, env, cont, val, true, false):
        self.expr = expr
        self.env = env
        self.cont = cont
        self.val = val
        self.true = true
        self.false = false

    def newExpr(self, expr, env, val):
        if val:
            return self.true
        else:
            return self.false

    def newEnv(self, expr, env, val):
        return self.env

    def newCont(self, expr, env, val):
        return self.cont

    def newVal(self, expr, env, val):
        return val

class Op1k(Contk):
    def __init__(self, expr, env, cont, val, op):
        self.expr = expr # Contains rhs
        self.env = env
        self.cont = cont
        self.val = val
        self.op = op

    def newExpr(self, expr, env, val):
        return self.expr

    def newEnv(self, expr, env, val):
        return self.env

    def newCont(self, expr, env, val):
        return Op2k(expr, env, self.cont, val, self.op)

    def newVal(self, expr, env, val):
        return val

class Op2k(Contk):
    def __init__(self, expr, env, cont, val, op):
        self.expr = expr
        self.env = env
        self.cont = cont
        self.val = val
        self.op = op

    def GetValAnsw(self,val):
        #It was only calculated once when I wanted to return tuples. Can't find better solution for now...
        left = self.val
        right = val
        
        if self.op == '+':
            return left + right
        elif self.op == '-':
            return left - right
        elif self.op == '*':
            return left * right
        elif self.op == '/':
            return left / right
        elif self.op == '%':
            return left % right
        elif self.op == '=':
            if left - right == 0:
                return 1
            else:
                return 0
        else:
            print("Parsing Error, symobl "+ self.op +" shouldn't be here.")
            return 2

    def newExpr(self, expr, env, val):
        valAnsw = self.GetValAnsw(val)
        return self.cont.newExpr(expr, env, valAnsw)

    def newEnv(self, expr, env, val):
        valAnsw = self.GetValAnsw(val)
        return self.cont.newEnv(expr, env, valAnsw)

    def newCont(self, expr, env, val):
        valAnsw = self.GetValAnsw(val)
        return self.cont.newCont(expr, env, valAnsw)

    def newVal(self, expr, env, val):
        valAnsw = self.GetValAnsw(val)
        return self.cont.newVal(expr, env, valAnsw)

class Appk(Contk):
    def __init__(self, expr, env, cont, val,arg):
        self.expr = expr # Contains body of function to apply
        self.env = env
        self.cont = cont
        self.val = val
        self.arg = arg

    def newExpr(self, expr, env, val):
        return self.expr

    def newEnv(self, expr, env, val):
        return {self.arg : val}

    def newCont(self, expr, env, val):
        return self.cont

    def newVal(self, expr, env, val):
        return val

              
#Interpret CPS - imperative


def Interpk(tree, funDict, env1):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    expr = tree
    env = env1
    cont = Idk() 
    val = None

    while not(isinstance(cont,Endk)):

        #
        if isinstance(expr, treeClass.Num):
            val = expr.n
            #
            expr2 = cont.newExpr(expr, env, val)
            env2 = cont.newEnv(expr, env, val)
            cont2 = cont.newCont(expr, env, val)
            val2 = cont.newVal(expr, env, val)
            expr = expr2
            env = env2
            cont = cont2
            val = val2
            
        #
        elif isinstance(expr, treeClass.Id):
            if expr.name in env.keys():
                val = (env[expr.name])
            else:
                print("Interpret Error: free identifier :\n" + tree.name)
            expr2 = cont.newExpr(expr, env, val)
            env2 = cont.newEnv(expr, env, val)
            cont2 = cont.newCont(expr, env, val)
            val2 = cont.newVal(expr, env, val)
            expr = expr2
            env = env2
            cont = cont2
            val = val2
        #
        elif isinstance(expr, treeClass.With):
            cont = Withk(expr, env, cont, val, expr.name, expr.body)
            expr = expr.nameExpr
        #
        elif isinstance(expr, treeClass.If):
            cont = Ifk(expr, env, cont, val, expr.ctrue, expr.cfalse)
            expr = expr.cond
        #
        elif isinstance(expr, treeClass.Op):
            cont = Op1k(expr.rhs, env, cont, val, expr.op)
            expr = expr.lhs
        #
        elif isinstance(expr, treeClass.App):
            if not expr.funName in funDict.keys():
                print("Inexistant function : "+expr.funName)
            fun = funDict[expr.funName]
            body = fun.body
            arg = fun.argName
            expr = expr.arg
            cont = Appk(body, env, cont, val, arg)
        #
        else: # Not an <F1WAE>
            print("Argument of Interpk is not a <F1WAE>:\n")
            cont = Endk(2)
    # End of while, cont meant to be Endk
    return cont.newVal(expr, env, val)
    
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
