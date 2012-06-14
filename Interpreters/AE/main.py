import writeExpr
import interpreter
import parser

def main(name="arithmeticExpr"):
    writeExpr.buildExpr(input("What depth do you want us to work on? (integer expected)\n"), name)
    with open(name,"r") as ae:
        expr = ae.read()
        print("The expression is:\n{}".format(expr))
        n = interpreter.interpretTree(parser.parser("".join(expr.split(" "))))
        print("The result is {}.".format(n))

#print("compile ok")
if __name__ == "__main__":
    import sys
    try:
        main(sys.argv[1])
    except IndexError:
        main()
