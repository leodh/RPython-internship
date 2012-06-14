import treeClass
import RPparser

def interpretTree(tree):
    if isinstance(tree, treeClass.Leaf):
        return tree.value
    elif isinstance(tree, treeClass.InsideNode):
        if tree.op == '+':
            return interpretTree(tree.leftSon) + interpretTree(tree.rightSon)
        else:
            return interpretTree(tree.leftSon) - interpretTree(tree.rightSon)
    else:
        raise ValueError("Node expected")

import os

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    #print("The expression is:\n" + (program_contents))
    n = interpretTree(RPparser.parser("".join(program_contents.split(" "))))
    print("The result is "+ str(n) + ".")

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
