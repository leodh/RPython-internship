# Parse and create AST based on RCFAE's BNF

import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from pypy.rlib.parsing.tree import Node, Nonterminal, Symbol

grammar = py.path.local().join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

# Tree classes

class RCFAE(object):
    """ For ineritance purpose only """
    
    def __init__(self):
        pass

    def __str__(self):
        pass

class ParsingError(RCFAE):
    def __init__(self):
        pass

    def __str__(self):
        return " ParsingError" 

class Num(RCFAE):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return ("( Num : %s )" % str(self.val))

class Id(RCFAE):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ("( Id : %s )" % self.name)

class Op(RCFAE):

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return ("( Op : %s %s %s )" % (self.lhs.__str__(), self.op, self.rhs.__str__() ))

class If(RCFAE):

    def __init__(self, cond, true, false):
        self.cond = cond
        self. true = true
        self.false = false

    def __str__(self):
        return ("( If : %s then %s else %s )" % (self.cond.__str__(), self.true.__str__(), self.false.__str__()) )

# Transformation from ebnf's tree structure to ours

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
        cond, true, false = ifTree.children[2], ifTree.children[3], ifTree.children[4]
        return If(self.visitRCFAE(cond), self.visitRCFAE(true), self.visitRCFAE(false))

    def visitRCFAE(self, tree):
        first = tree.children[0]
             
        if first.symbol == "__0_{":
            first = tree.children[1]

        if isinstance(first, Symbol):
            return self.visitSymbol(first)
        else:
            if first.symbol == "op":
                return self.visitOp(tree)
            elif first.symbol =="if":
                return self.visitIf(tree)
            else:
                return ParsingError()
                
        
        
# Main instructions

def Main(source):
    tree = _parse(source)
    transforme = Transformer()
    ourTree = transforme.visitRCFAE(tree)
    print ourTree.__str__()
    print(42)

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

