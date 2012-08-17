import parser

# Return type

class ReturnType(object):

    def __init__(self):
        pass

    def __str__(self):
        pass

class NumV(ReturnType):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def add(self, other):
        assert isinstance(other, NumV)
        return NumV(self.val + other.val)

    def diff(self, other):
        assert isinstance(other, NumV)
        return NumV(self.val - other.val)

    def mult(self, other):
        assert isinstance(other, NumV)
        return NumV(self.val * other.val)

    def div(self, other):
        assert isinstance(other, NumV)
        return NumV(self.val / other.val)

    def mod(self, other):
        assert isinstance(other, NumV)
        return NumV(self.val % other.val)


# Interpreter

def Interpret(tree):

    if isinstance(tree, parser.Num):
        return NumV(tree.val)

    elif isinstance(tree, parser.Op):
        if tree.op == '+':
            Lhs = Interpret(tree.lhs)
            assert isinstance(Lhs, NumV)
            return Lhs.add(Interpret(tree.rhs))
        elif tree.op == '-':
            Lhs = Interpret(tree.lhs)
            assert isinstance(Lhs, NumV)
            return Lhs.diff(Interpret(tree.rhs))
        elif tree.op == '*':
            Lhs = Interpret(tree.lhs)
            assert isinstance(Lhs, NumV)
            return Lhs.mult(Interpret(tree.rhs))
        elif tree.op == '/':
            Lhs = Interpret(tree.lhs)
            assert isinstance(Lhs, NumV)
            return Lhs.div(Interpret(tree.rhs))
        elif tree.op == '%':
            Lhs = Interpret(tree.lhs)
            assert isinstance(Lhs, NumV)
            return Lhs.mod(Interpret(tree.rhs))
        else:
            return ReturnType()
        
    else:
        print "Parsing error, tree %s is not valid" % tree.__str__()
        return ReturnType()

            
# Main instructions

def Main(source):
    tree = parser._parse(source)
    transforme = parser.Transformer()
    ourTree = transforme.visitRCFAE(tree)
    print ourTree.__str__()
    answer = Interpret(ourTree)
    print answer.__str__()

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
