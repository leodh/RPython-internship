import treeClass
import parser

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

if __name__ == "__main__":
    import sys
    try:
        with open(sys.argv[1],"r") as ae:
                    expr = ae.read()
        #print("The expression is:\n{}".format(expr))
        n = interpretTree(parser.parser("".join(expr.split(" "))))
        print("The result is {}.".format(n))
    except IndexError:
        print("You must supply a file to interpret")
