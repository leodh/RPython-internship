import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
#from usingEBNF import usingEBNFdir

grammar = py.path.local().join("grammar.txt").read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

# <file> ::= <Func>* <Proc> <Func>*

# <Func> ::= { ( <id> <id> )
#                <ifF1WAE>  } 


# <Proc> :: = <num>
#          | ( <op> <Proc> <Proc> )
#          | ( with ( <id> <Proc> ) <Proc> )
#          | <id>
#          | ( <id> <Proc>)
#          | ( if <Proc> <Proc> <Proc> ) # (if <cond> <true> <false>) True <=> !=0

# <op> ::= '+' | '-' | '*' | '/' | '%' | '='
# <num> ::= [ '0' - '9' ]+
# <id> ::= [ '_', 'a' - 'z', 'A' - 'Z'][ '_', 'a' - 'z', 'A' - 'Z', '0' -'9' ]*



class Func:
    def __init__(self, name, argName, body):
        self.name=name # Id
        self.argName=argName # Id
        self.body=body # ifF1WAE

class NoneFunc(Func):
    """Useful for GetFunc in Interpreter"""
    
    def __init__(self):
        pass

class ifF1WAE:
    def __init__(self):
        pass
        
class Node(ifF1WAE):
    def __init__(self):
        pass

class Leaf(ifF1WAE):
    def __init__(self):
        pass

class Num(Leaf):
    _immutable_fields_ = ["n"]
    def __init__(self, n):
        self.n=n # Int

class Id(Leaf):
    _immutable_fields_ = ["name"]
    def __init__(self, name):
        self.name=name # Id

class Op(Node):
    _immutable_fields_ = ["op", "lhs", "rhs"]
    def __init__(self, op, lhs, rhs):
        self.op=op # Op
        self.lhs=lhs # ifF1WAE
        self.rhs=rhs # ifF1WAE

class With(Node):
    _immutable_fields_ = ["name", "nameExpr", "body"]
    def __init__(self, name, nameExpr, body):
        self.name=name # Id
        self.nameExpr=nameExpr # ifF1WAE
        self.body=body # ifF1WAE

class App(Node):
    _immutable_fields_ = ["funName", "arg"]
    def __init__(self, funName, arg):
        self.funName=funName # Id, name of a function
        self.arg=arg # ifF1WAE

class If(Node):
    _immutable_fields_ = ["cond", "ctrue", "cfalse"]
    def __init__(self, cond, ctrue, cfalse):
        self.cond=cond # Condition
        self.ctrue=ctrue # If condition is true
        self.cfalse=cfalse #If condition is false
        
def treePrint(tree):
    """ Pretty printing a tree """

    if isinstance(tree, Num):
        return("Num " + str(tree.n))
        
    elif isinstance(tree, Id):
        return("Id " + tree.name)

    elif isinstance(tree, Op):
        return("Op " + str(tree.op))

    elif isinstance(tree, With):
        return("With " + tree.name)

    elif isinstance(tree, App):
        return("App "+ tree.funName)

    elif isinstance(tree, If):
        return("If "+ treePrint(tree.cond))

    else:
        return("Not a ifF1WAE!")
        

def Main(source):
    x = _parse(source)
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
