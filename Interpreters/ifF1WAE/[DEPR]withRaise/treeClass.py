# <file> ::= <Def>* <Prog> <Def>*

# <Prog> ::= <F1WAE>

# <Def> ::= { ( <id> <id> )
#                ( <F1WAE> ) } 


# <F1WAE> :: = <num>
#          | ( <op> <F1WAE> <F1WAE> )
#          | ( with ( <id> <F1WAE> ) <F1WAE> )
#          | <id>
#          | ( <id> <F1WAE>)
#          | ( if <F1WAE> <F1WAE> <F1WAE> ) # (if <cond> <true> <false>) True <=> !=0

# <op> ::= '+' | '-' | '*' | '/' | '%' | '='
# <num> ::= [ '0' - '9' ]+
# <id> ::= [ '_', 'a' - 'z', 'A' - 'Z'][ '_', 'a' - 'z', 'A' - 'Z', '0' -'9' ]*

class File:
    def __init__(self, prog, funcDic):
        self.prog=prog #Should be a F1WAE
        self.funcDic=funcDic #Should be a dictionnary of keys name_of_function and values of class Func

class Func:
    def __init__(self, name, argName, body):
        self.name=name # Id
        self.argName=argName # Id
        self.body=body # F1WAE

class F1WAE:
    def __init__(self):
        pass
        
class Node(F1WAE):
    def __init__(self):
        pass

class Leaf(F1WAE):
    def __init__(self):
        pass

class Num(Leaf):
    def __init__(self, n):
        self.n=n # Int

class Id(Leaf):
    def __init__(self, name):
        self.name=name # Id

class Op(Node):
    def __init__(self, op, lhs, rhs):
        self.op=op # Op
        self.lhs=lhs # F1WAE
        self.rhs=rhs # F1WAE

class With(Node):
    def __init__(self, name, nameExpr, body):
        self.name=name # Id
        self.nameExpr=nameExpr # F1WAE
        self.body=body # F1WAE

class App(Node):
    def __init__(self, funName, arg):
        self.funName=funName # Id, name of a function
        self.arg=arg # F1WAE

class If(Node):
    def __init__(self, cond, ctrue, cfalse):
        self.cond=cond # Condition
        self.ctrue=ctrue # If condition is true
        self.cfalse=cfalse #If condition is false
        
        
