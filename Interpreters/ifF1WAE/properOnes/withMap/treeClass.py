# <file> ::= <Def>* <Prog> <Def>*

# <Prog> ::= <ifF1WAE>

# <Def> ::= { ( <id> <id> )
#                ( <ifF1WAE> ) } 


# <ifF1WAE> :: = <num>
#          | ( <op> <ifF1WAE> <ifF1WAE> )
#          | ( with ( <id> <ifF1WAE> ) <ifF1WAE> )
#          | <id>
#          | ( <id> <ifF1WAE>)
#          | ( if <ifF1WAE> <ifF1WAE> <ifF1WAE> ) # (if <cond> <true> <false>) True <=> !=0

# <op> ::= '+' | '-' | '*' | '/' | '%' | '='
# <num> ::= [ '0' - '9' ]+
# <id> ::= [ '_', 'a' - 'z', 'A' - 'Z'][ '_', 'a' - 'z', 'A' - 'Z', '0' -'9' ]*

from pypy.rlib.jit import elidable

class File:
    def __init__(self, prog, funcDic):
        self.prog=prog #Should be a ifF1WAE
        self.funcMap=funcMap #Should be a map of keys name_of_function and values of class Func

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
        
#######
# Map #
#######

class MapEnv(object):
    def __init__(self):
        self.values = {}
        self.other_maps = {}

    @elidable
    def getvalues(self, name):
        return self.values.get(name, 2)

    @elidable
    def add_attribute(self, name, value):
        if name not in self.other_maps:
            newmap = MapEnv()
            newmap.values.update(self.values)
            newmap.values[name] = value
            self.other_maps[name] = newmap
        return self.other_maps[name]

EMPTY_MAP_ENV = MapEnv()

class MapFunc(object):
    def __init__(self):
        self.funcs = {}
        self.other_maps = {}

    @elidable
    def getfuncs(self, name):
        return self.funcs.get(name, NoneFunc())

    @elidable
    def add_attribute(self, name, descr):
        if name not in self.other_maps:
            newmap = MapFunc()
            newmap.funcs.update(self.funcs)
            newmap.funcs[name] = descr
            self.other_maps[name] = newmap
        return self.other_maps[name]

EMPTY_MAP_FUNC = MapFunc()