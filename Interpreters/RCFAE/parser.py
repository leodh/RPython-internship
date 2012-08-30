from pypy.rlib.jit import promote, elidable

#############################################
# Parse and create AST based on RCFAE's BNF #
#############################################

import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from pypy.rlib.parsing.tree import Node, Nonterminal, Symbol

grammar = py.path.local().join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

################
# Tree classes #
################

class RCFAE(object):
    """ For ineritance purpose only """
    
    def __init__(self):
        pass

    def __str__(self):
        return "Root type RCFAE"

    def printable(self):
        return self.__str__()

class ParsingError(RCFAE):
    """ To deal with errors """
    
    def __init__(self):
        pass

    def __str__(self):
        return " ParsingError" 

    def printable(self):
        return self.__str__()
    
class Num(RCFAE):
    _immutable_fields_ = [ "val" ]
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return ("( Num : %s )" % str(self.val))

    def printable(self):
        return self.__str__()
            

class Id(RCFAE):
    _immutable_fields_ = [ "name" ]
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ("( Id : %s )" % self.name)

    def printable(self):
        return self.__str__()

class Op(RCFAE):
    _immutable_fields_ = [ "op", "lhs", "rhs" ]
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return ("( Op : %s %s %s )" % (self.lhs.__str__(), self.op, self.rhs.__str__() ))

    def printable(self):
        return "( Op : %s )" % self.op
    
class If(RCFAE):
    _immutable_fields_ = [ "nul", "true", "false" ]
    def __init__(self, nul, true, false):
        self.nul = nul
        self. true = true
        self.false = false

    def __str__(self):
        return ("( If : %s == 0 then %s else %s )" % (self.nul.__str__(), self.true.__str__(), self.false.__str__()) )

    def printable(self):
        return "( If0 : %s )" % self.nul.printable()
        
class Func(RCFAE):
    _immutable_fields_ = [ "arg", "body" ]
    def __init__(self, arg, body):
        self.arg = arg
        self.body = body

    def __str__(self):
        return ("( Fun : (%s) %s )" % (self.arg.__str__(), self.body.__str__()) )

    def printable(self):
        return "( Fun : (%s) %s)" % (self.arg.__str__(), self.body.printable())

class App(RCFAE):
    _immutable_fields_ = [ "fun", "arg" ]
    def __init__(self, fun, arg):
        self.fun = fun
        self.arg = arg

    def __str__(self):
        return ("( App : %s %s )" % (self.fun.__str__(), self.arg.__str__()))

    def printable(self):
        return "( App : %s %s)" % (self.fun.printable(), self.arg.printable())

class Rec(RCFAE):
    _immutable_fields_ = [ "funName", "body", "expr" ]
    def __init__(self, funName, body, expr):
        self.funName = funName
        self.body = body
        self.expr = expr

    def __str__(self):
        return ("( Rec : ( FunDef : %s:%s) %s)" % ( self.funName, self.body.__str__(), self.expr.__str__() ))

    def printable(self):
        return "( Rec : ( %s ) %s)" % (self.funName, self.expr.printable())

#####################################################
# Transformation from ebnf's tree structure to ours #
#####################################################
    
class Transformer(object):
    """Transforme a tree in ebnf's structure to ours"""

    def __init__(self):
        pass

    def visitSymbol(self, symb):
        val = symb.additional_info
        if symb.symbol == "NUM":
            return Num(int(val))
        elif symb.symbol == "ID":
            return Id(val)
        else: # Case OP not treated here, must be detected elsewhere
            return ParsingError()

    def visitOp(self, opTree):
        op, lhs, rhs = opTree.children[1], opTree.children[2], opTree.children[3]
        return Op(str((op.children[0]).additional_info), self.visitRCFAE(lhs), self.visitRCFAE(rhs))

    def visitIf(self, ifTree):
        nul, true, false = ifTree.children[2], ifTree.children[3], ifTree.children[4]
        return If(self.visitRCFAE(nul), self.visitRCFAE(true), self.visitRCFAE(false))

    def visitFunc(self, funcTree):
        arg, body = funcTree.children[3], funcTree.children[5]
        return Func(self.visitSymbol(arg), self.visitRCFAE(body))

    def visitApp(self, appTree):
        fun, arg = appTree.children[1], appTree.children[2]
        return App(self.visitRCFAE(fun), self.visitRCFAE(arg))

    def visitRec(self, recTree):
        funName, body, expr = recTree.children[3], recTree.children[4], recTree.children[6]
        return Rec( funName.additional_info, self.visitRCFAE(body), self.visitRCFAE(expr) )

    def visitRCFAE(self, tree):
        first = tree.children[0]
             
        if first.symbol == "__0_{":
            first = tree.children[1]

        if isinstance(first, Symbol):
            return self.visitSymbol(first)
        else:
            if first.symbol == "op":
                return self.visitOp(tree)
            elif first.symbol == "if":
                return self.visitIf(tree)
            elif first.symbol == "fun":
                return self.visitFunc(tree)
            elif first.symbol == "rcfae":
                return self.visitApp(tree)
            elif first.symbol == "rec":
                return self.visitRec(tree)
            else:
                return ParsingError() 
        
 
