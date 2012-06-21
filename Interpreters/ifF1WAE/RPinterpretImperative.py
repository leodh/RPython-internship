import treeClass
import parser
import sys


#Class Function for CPS

class Contk:
    def __init__(self,*arg):
        raise NotImplementedError("For abstract class")
    
    def apply(self,expr,env,cont,val,proc):
        return expr, env, cont, val, proc

# TO IMPLEMENT
#
# class Idk(Funck):
#     def __init__(self):
#         pass
    
#     def apply(self,arg):
#         return arg

# class Opk(Funck):
#     def __init__(self,argLeft,op,k):
#         self.argLeft=argLeft
#         self.op=op
#         self.k=k


#     def apply(self,arg):
#         if self.op == '+':
#             return self.k.apply(self.argLeft + arg)
#         elif self.op == '-':
#             return self.k.apply(self.argLeft - arg)
#         elif self.op == '*':
#             return self.k.apply(self.argLeft * arg)
#         elif self.op == '/':
#             return self.k.apply(self.argLeft / arg)
#         elif self.op == '%':
#             return self.k.apply(self.argLeft % arg)
#         elif self.op == '=':
#             if self.argLeft - arg == 0:
#                 return self.k.apply(1)
#             else:
#                 return self.k.apply(0)
#         else:
#             print("Parsing Error, symobl "+ self.op +" shouldn't be here.")
#             return 2

# class OpLeftk(Funck):
#     def __init__(self, exprRight, funDict, env, k, op):
#         self.exprRight=exprRight
#         self.funDict=funDict
#         self.env=env
#         self.k=k
#         self.op=op

#     def apply(self, arg):
#         return Interpk(self.exprRight,self.funDict,self.env, Opk(arg,self.op,self.k))

# class Appk(Funck):
#     def __init__(self, funName, funDict, k):
#         self.funName=funName
#         self.funDict=funDict
#         self.k=k

#     def apply(self, arg):
#         if self.funName in self.funDict.keys():
#             g=self.funDict[self.funName]
#             return Interpk(g.body,self.funDict, {g.argName: arg}, self.k)
#         else:
#             print("Invalid function : " + self.funName)
#             return 2


# class Ifk(Funck):
#     def __init__(self, true, false, funDict, env, k):
#         self.true=true
#         self.false=false
#         self.funDict=funDict
#         self.env=env
#         self.k=k

#     def apply(self,arg):
#         if arg != 0:
#             return Interpk(self.true, self.funDict, self.env, self.k)
#         else:
#             return Interpk(self.false, self.funDict, self.env, self.k)


#Interpret CPS - imperative


def Interpk(tree, funDict, env1)
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    expr = tree
    env = env1
    cont = Endk() # Continuation de fin
    val = None
    proc = None

    #value-of/k
    while \ # Condition à determiner
        True :

        #
        if isinstance(env, treeClass.Num):
            val = tree.n
            ex, en, co, va, pr = cont.apply(expr,env,val,proc) # apply-cont
            expr = en
            env = en
            cont = co
            val = va
            proc = pr
        #
        elif isinstance(tree, treeClass.Id):
            if tree.name in env.keys():
                var = (env[tree.name])
            else:
                print("Interpret Error: free identifier :\n" + tree.name)
            ex, en, co, va, pr = cont.apply(expr,env,val,proc) # Besoin des 5: selon le cas certains resteront inchangé, d'autres non, pour rester général, les fonction apply prennent tout en argument et renvoient tout
            expr = en
            env = en
            cont = co
            val = va
            proc = pr
        #
        elif isinstance(tree, treeClass.With):
            cont = Withk(expr, env, cont, val, cont, tree.name, tree.body)
            expr = tree.nameExpr
        #
        elif isinstance(tree, treeClass.If):
            cont = Ifk(expr, env, cont, val, proc, tree.true, tree.false)
            expr = tree.cond
        #
        elif isinstance(tree, treeClass.Op):
            cont = Op1k(expr, env, cont, val, proc, tree.op, tree.rhs)
            expr = tree.lhs
        #
        elif isinstance(tree, treeClass.App):
            cont = Ratork(expr, env, cont, val, proc, tree.arg)
            if tree.funName in funDict.key():
                expr = funDict[tree.funName]
            else:
                print("Inexistant function : "+tree.funName)
        #
        else: # Not an <F1WAE>
            print("Argument of Interpk is not a <F1WAE>:\n")
    #
    
def Main(file):
    t,d = parser.Parse(file)
    j = Interpk(t,d,{},Idk())
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
