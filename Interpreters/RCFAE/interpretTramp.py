import parser

from pypy.rlib.jit import JitDriver, elidable, promote

#######################################
# Map for environement representation #
#######################################

class Map(object):
    def __init__(self):
        self.values = {}

    @elidable
    def getvalue(self, name):
        return self.values.get(name, ErrorV("Free variable : %s" % name))

    @elidable
    def add_attribute(self, name, value):
        newmap = Map()
        newmap.values.update(self.values)
        newmap.values[name] = value
        return newmap

    def __str__(self):
        str = "Map : \n"
        for i in self.values.keys():
            str += "(\n %s, \n %s\n)\n" % (i,(self.values[i].__str__()))
        return str

###############
# Return type #
###############

class ReturnType(object):
    """ Class of objects returned by the Interpret function.
    For Inheritance."""

    def __init__(self):
        pass

    def __str__(self):
        pass

class ErrorV(ReturnType):
    """ In case an error occurs """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

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
        return "Wrong return type for expression :\n %s\n Should be of type NumV." % tree.__str__()
    else:
        return "True"

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
        return "Wrong return type for expression :\n %s\n Should be of type ClosureV." % tree.__str__()
    else:
        return "True"

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
        return FinalBounce(x)

class Op1K(Continuation):

    def __init__(self, op, lhs, rhs, env, k):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.env = env
        self.k = k

    def _apply(self, Lhs):
        msg = assertNumV(Lhs, self.lhs)
        if msg != "True":
            return FinalBounce(ErrorV(msg))
        k = Op2K(Lhs, self.op, self.rhs, self.k)
        return KeepBouncing(self.rhs, self.env, k)

class Op2K(Continuation):

    def __init__(self, Lhs, op, rhs, k):
        self.Lhs = Lhs
        self.op = op
        self.rhs = rhs
        self.k = k

    def _apply(self, Rhs):
        msg = assertNumV(Rhs, self.rhs)
        if msg != "True":
            return FinalBounce(ErrorV(msg))

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
            msg = "Parsing error, operator %s not valid" % self.op
            return FinalBounce(ErrorV(msg))

class If0K(Continuation):

    def __init__(self, nul, true, false, env, k):
        self.nul = nul
        self.true = true
        self.false = false
        self.env = env
        self.k = k

    def _apply(self, nul):
        msg = assertNumV(nul, self.nul)
        if msg  != "True":
            return FinalBounce(ErrorV(msg))
        if nul.val == 0:
            return KeepBouncing(self.true, self.env, self.k)
        else:
            return KeepBouncing(self.false, self.env, self.k)

class App1K(Continuation):

    def __init__(self, fun, env, k):
        self.fun = fun
        self.env = env
        self.k = k

    def _apply(self, arg):
        newK = App2K(self.fun, arg, self.k)
        return KeepBouncing(self.fun, self.env, newK)

class App2K(Continuation):

    def __init__(self, fun, arg, k):
        self.fun = fun
        self.arg = arg
        self.k = k

    def _apply(self, fun):
        msg = assertClosureV(fun, self.fun)
        if msg != "True":
            return FinalBounce(ErrorV(msg))
        param = fun.arg
        assert isinstance(param, parser.Id)
        newEnv = fun.env
        promote(newEnv)
        newEnv = newEnv.add_attribute(param.name, self.arg)
        return KeepBouncing(fun.body, newEnv, self.k)
        

class RecK(Continuation):

    def __init__(self, funName, body, expr, k):
        self.funName = funName
        self.body = body
        self.expr = expr
        self.k = k

    def _apply(self, funDef):
        msg = assertClosureV(funDef, self.body)
        if msg != "True":
            return FinalBounce(ErrorV(msg))
        newEnv = funDef.env
        promote(newEnv)
        funDef.env = newEnv.add_attribute(self.funName, funDef)
        return KeepBouncing(self.expr, funDef.env, self.k) 


##############
# Trampoline #
##############

class Bounce(object):
    """ For inheritance purpose """

    def __init__(self):
        pass

    def __str__(self):
        return "Root class"

    def bounce(self):
        pass

class FinalBounce(Bounce):
    """ Indicates end of loop and work """

    def __init__(self, answ):
        self.answ = answ

    def __str__(self):
        return self.answ.__str__()

    def bounce(self):
        return self.answ

class KeepBouncing(Bounce):

    def __init__(self, tree, env, k):
        self.tree = tree
        self.env = env
        self.k = k

    def __str__(self):
        return self.tree.__str__()

    def bounce(self):

        tree = self.tree
        env = self.env
        k = self.k
        
        if isinstance(tree, parser.Num):
            return k._apply(NumV(tree.val))

        elif isinstance(tree, parser.Op):
            newK = Op1K(tree.op, tree.lhs, tree.rhs, env, k)
            return KeepBouncing(tree.lhs, env, newK)
        
        elif isinstance(tree, parser.Id):
            promote(env)
            val = env.getvalue(tree.name)
            if isinstance(val, ErrorV):
                return FinalBounce(val)
            else:
                return k._apply(val)

        elif isinstance(tree, parser.If):
            newK = If0K(tree.nul, tree.true, tree.false, env, k)
            return KeepBouncing(tree.nul, env, newK)

        elif isinstance(tree, parser.Func):
            assert isinstance(tree.arg, parser.Id)
            return k._apply(ClosureV(tree.arg, tree.body, env))

        elif isinstance(tree, parser.App):
            newK = App1K(tree.fun, env, k)
            return KeepBouncing(tree.arg, env, newK)

        elif isinstance(tree, parser.Rec):
            newK = RecK(tree.funName, tree.body, tree.expr, k)
            dummy = NumV(42)
            promote(env)
            env = env.add_attribute(tree.funName, dummy)
            return KeepBouncing(tree.body, env, newK)

        else:
            msg = "Parsing error, tree %s is not valid" % tree.__str__()
            return FinalBounce(ErrorV(msg))


###############
# Interpreter #
###############

# JITing instructions

def get_printable_location(tree):
    return tree.__str__()

jitdriver = JitDriver(greens=['tree'], reds=['env', 'k', 'bouncer'], get_printable_location=get_printable_location)
    

def Interpret(tree):
    """Interpret the tree."""

    env = Map()
    k = EndK()
    bouncer = KeepBouncing(tree, env, k)

    while 1:
        jitdriver.jit_merge_point(tree=tree, env=env, k=k, bouncer=bouncer)
        
        if isinstance(bouncer, FinalBounce):
            break
        elif isinstance(bouncer, KeepBouncing):
            tree = bouncer.tree
            env = bouncer.env
            k = bouncer.k
            bouncer = bouncer.bounce()
            jitdriver.can_enter_jit(tree=tree, env=env, k=k, bouncer=bouncer)
        else:
            bouncer = FinalBounce( ErrorV(" Bouncer not a bounce ?!"))

    assert isinstance(bouncer, FinalBounce)
    return bouncer.bounce()


#####################            
# Main instructions #
#####################

def Main(source):
    """Main function."""
    
    tree = parser._parse(source)
    transforme = parser.Transformer()
    ourTree = transforme.visitRCFAE(tree)
    #    print ourTree.__str__()
    answer = Interpret(ourTree)
    print answer.__str__()

import os

def jitpolicy(driver):
    from pypy.jit.codewriter.policy import JitPolicy
    return JitPolicy()

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
