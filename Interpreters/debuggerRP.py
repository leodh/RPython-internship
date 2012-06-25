import os
import sys

class Contk:
    def __init__(self,*arg):
        raise NotImplementedError("For abstract class")
    
    def apply(self,expr,env,val):
        raise NotImplementedError("For abstract class")


class Endk(Contk):
    def __init__(self,val):
        self.val = val

    def apply(self,expr, env, val):
        return self.val

class Idk(Contk):
    def __init__(self):
        pass
    
    def apply(self, expr, env, val):
        return expr, env, Endk(val), val

def Main():
    return "ok"

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    print(Main())

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
