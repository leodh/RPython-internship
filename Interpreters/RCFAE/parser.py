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

class Num(RCFAE):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return ("( Num : % )" % self.val)

class Id(RCFAE):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ("( Id : %)" % self.name)

class Op(RCFAE):

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return ("Op : % % %" % (self.lhs.__str__, self.op, self.rhs.__str__))

# Transformation from ebnf's tree structure too ours

class Transformer(object):
    """Transforme a tree in ebnf's structure to ours"""

    def __init__(self):
        pass

    def visitSymbol(self, symb):
        val = symb.children[0]
        if symb.symbol == "NUM":
            return Num(int(val))
        elif symb.symbol == "ID":
            return Id(val)
        else: # Case OP not treated here, must be detected elsewhere
            return ParsingError()

        
# Main instructions

def Main(source):
    tree = _parse(source)
    print(tree.__str__())
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

