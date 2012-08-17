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
        return NumV(self.val + other.val)

    def diff(self, other):
        return NumV(self.val - other.val)

    def mult(self, other):
        return NumV(self.val * other.val)

    def div(self, other):
        return NumV(self.val / other.val)

    def mod(self, other):
        return NumV(self.val % other.val)


# Interpreter

def Interpret(tree, env):

    if isinstance(tree, parser.Num):
        return NumV(tree.val)

    elif isinstance(tree, parser.Op):
        Lhs = Interpret(tree.lhs, env)
        if not isinstance(Lhs, NumV):
            print "Wrong return type for expression :\n %s\n Should be of type NumV." % tree.lhs.__str__()
            return ReturnType()
        Rhs = Interpret(tree.rhs, env)
        if not isinstance(Rhs, NumV):
            print "Wrong return type for expression :\n %s\n Should be of type NumV." % tree.rhs.__str__()
            return ReturnType()
        else:
            if tree.op == '+':
                return Lhs.add(Rhs)
            elif tree.op == '-':
                return Lhs.diff(Rhs)
            elif tree.op == '*':
                return Lhs.mult(Rhs)
            elif tree.op == '/':
                return Lhs.div(Rhs)
            elif tree.op == '%':
                return Lhs.mod(Rhs)
            else:
                print "Parsing error, operator %s not valid" % tree.op
                return ReturnType()

    elif isinstance(tree, parser.Id):
        print "Not implemented yet"
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
    env = parser.Env()
    answer = Interpret(ourTree, env)
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
