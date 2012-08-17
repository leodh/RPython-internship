import parser

###############
# Return type #
###############

class ReturnType(object):
    """ Class of objects returned by the Interpret function."""

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


def assertNumV(expr, tree):
    """ Assert class of expr is NumV, else blame tree."""
    
    if not isinstance(expr, NumV):
        print "Wrong return type for expression :\n %s\n Should be of type NumV." % tree.__str__()
        return False
    else:
        return True

class ClosureV(ReturnType):

    def __init__(self, arg, body, env):
        self.arg = arg
        self.body = body
        self.env = env

    def __str__(self):
        return "(fun : %s |-> %s)" % (self.arg.__str__(), self.body.__str__())

def assertClosureV(expr, tree):
    """ Assert class of expr is ClosureV, else blame tree."""
    
    if not isinstance(expr, ClosureV):
        print "Wrong return type for expression :\n %s\n Should be of type ClosureV." % tree.__str__()
        return False
    else:
        return True

#################
# Continuations #
#################

class Continuation(object):
    """ Super class, for inheritance purpose only."""

    def __init__(self):
        pass

class EndK(Continuation):

    def __init__(self):
        pass

    def _apply(self, x):
        return x

class Op1K(Continuation):

    def __init__(self, op, lhs, rhs, env, k):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.env = env
        self.k = k

    def _apply(self, Lhs):
        if not assertNumV(Lhs, self.lhs):
            return ReturnType()
        k = Op2K(Lhs, self.op, self.rhs, self.k)
        return Interpret(self.rhs, self.env, k)

class Op2K(Continuation):

    def __init__(self, Lhs, op, rhs, k):
        self.Lhs = Lhs
        self.op = op
        self.rhs = rhs
        self.k = k

    def _apply(self, Rhs):
        if not assertNumV(Rhs, self.rhs):
            return ReturnType()

        if self.op == '+':
            return self.k._apply(self.Lhs.add(Rhs))
        elif self.op == '-':
            return self.k._apply(self.Lhs.diff(Rhs))
        elif self.op == '*':
            return self.k._apply(self.Lhs.mult(Rhs))
        elif self.op == '/':
            return self.k._apply(self.Lhs.div(Rhs))
        elif self.op == '%':
            return self.k._apply(self.Lhs.mod(Rhs))
        else:
            print "Parsing error, operator %s not valid" % self.op
            return ReturnType()        

###############
# Interpreter #
###############

def Interpret(tree, env, k):
    """Interpret the tree, given an environment."""

    if isinstance(tree, parser.Num):
        return k._apply(NumV(tree.val))

    elif isinstance(tree, parser.Op):
        newK = Op1K(tree.op, tree.lhs, tree.rhs, env, k)
        return Interpret(tree.lhs, env, newK)
        
    # elif isinstance(tree, parser.Id):
    #     try:
    #         return env.get_attr(tree.name)
    #     except parser.FreeVariable as FV:
    #         print "Free variable : %s" % FV.__str__()
    #         return ReturnType()

    # elif isinstance(tree, parser.If):
    #     nul = Interpret(tree.nul, env)
    #     if not assertNumV(nul, tree.nul):
    #         return ReturnType()
    #     if nul.val == 0:
    #         return Interpret(tree.true, env)
    #     else:
    #         return Interpret(tree.false, env)

    # elif isinstance(tree, parser.Func):
    #     assert isinstance(tree.arg, parser.Id)
    #     return ClosureV(tree.arg, tree.body, env)

    # elif isinstance(tree, parser.App):
    #     fun = Interpret(tree.fun, env)
    #     if not assertClosureV(fun, tree.fun):
    #         return ReturnType()
    #     arg = Interpret(tree.arg, env)
    #     newEnv = fun.env
    #     param = fun.arg
    #     assert isinstance(param, parser.Id)
    #     newEnv.write_attribute(param.name, arg)
    #     return Interpret(fun.body, newEnv)

    # elif isinstance(tree, parser.Rec):
    #     dummy = NumV(42)
    #     env.write_attribute(tree.funName, dummy)
    #     funDef = Interpret(tree.body, env)
    #     if not assertClosureV(funDef, tree.body):
    #         return ReturnType()
    #     newEnv = funDef.env
    #     newEnv.write_attribute(tree.funName, funDef)
    #     funDef.env = newEnv
    #     return Interpret(tree.expr, newEnv)
    
    else:
        print "Parsing error, tree %s is not valid" % tree.__str__()
        return ReturnType()

#####################            
# Main instructions #
#####################

def Main(source):
    """Main function."""
    
    tree = parser._parse(source)
    transforme = parser.Transformer()
    ourTree = transforme.visitRCFAE(tree)
    print ourTree.__str__()
    env = parser.Env()
    answer = Interpret(ourTree, env, EndK())
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
