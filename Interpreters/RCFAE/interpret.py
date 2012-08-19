import parser

###############
# Return type #
###############

class ReturnType(object):
    """ Class of objects returned by the Interpret function.
    For Inheritance and errors."""

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

class If0K(Continuation):

    def __init__(self, nul, true, false, env, k):
        self.nul = nul
        self.true = true
        self.false = false
        self.env = env
        self.k = k

    def _apply(self, nul):
        if not assertNumV(nul, self.nul):
            return ReturnType()
        if nul.val == 0:
            return Interpret(self.true, self.env, self.k)
        else:
            return Interpret(self.false, self.env, self.k)

class App1K(Continuation):

    def __init__(self, fun, arg, env, k):
        self.fun = fun
        self.arg = arg
        self.env = env
        self.k = k

    def _apply(self, fun):
        if not assertClosureV(fun, self.fun):
            return ReturnType()
        newK = App2K(fun, self.env, self.k)
        return Interpret(self.arg, self.env, newK)

class App2K(Continuation):

    def __init__(self, fun, env, k):
        self.fun = fun
        self.env = env
        self.k = k

    def _apply(self, arg):
        param = self.fun.arg
        assert isinstance(param, parser.Id)
        newEnv = self.env
        newEnv.write_attribute(param.name, arg)
        return Interpret(self.fun.body, newEnv, self.k)
        

class RecK(Continuation):

    def __init__(self, funName, body, expr, k):
        self.funName = funName
        self.body = body
        self.expr = expr
        self.k = k

    def _apply(self, funDef):
        if not assertClosureV(funDef, self.body):
            return ReturnType()
        newEnv = funDef.env
        newEnv.write_attribute(self.funName, funDef)
        funDef.env = newEnv
        return Interpret(self.expr, funDef.env, self.k) 


##############
# Trampoline #
##############

class Bounce(object):
    """ For inheritance purpose """

    def __init__(self):
        pass

class FinalBounce(Bounce):
    """ Indicates end of loop and work """

    def __init__(self, answ):
        self.answ = answ

    def bounce(self):
        return self.answ


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
        
    elif isinstance(tree, parser.Id):
        try:
            return k._apply(env.get_attr(tree.name))
        except parser.FreeVariable as FV:
            print "Free variable : %s" % FV.__str__()
            return ReturnType()

    elif isinstance(tree, parser.If):
        newK = If0K(tree.nul, tree.true, tree.false, env, k)
        return Interpret(tree.nul, env, newK)


    elif isinstance(tree, parser.Func):
        assert isinstance(tree.arg, parser.Id)
        return k._apply(ClosureV(tree.arg, tree.body, env))

    elif isinstance(tree, parser.App):
        newK = App1K(tree.fun, tree.arg, env, k)
        return Interpret(tree.fun, env, newK)

    elif isinstance(tree, parser.Rec):
        newK = RecK(tree.funName, tree.body, tree.expr, k)
        dummy = NumV(42)
        env.write_attribute(tree.funName, dummy)
        return Interpret(tree.body, env, newK)
    
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
