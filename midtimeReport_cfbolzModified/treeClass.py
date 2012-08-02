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

class File:
    def __init__(self, prog, funcDic):
        self.prog=prog #Should be a ifF1WAE
        self.funcDic=funcDic #Should be a dictionnary of keys name_of_function and values of class Func

class Func:
    def __init__(self, name, argName, body):
        self.name=name # Id
        self.argName=argName # Id
        self.body=body # ifF1WAE

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
        
        
