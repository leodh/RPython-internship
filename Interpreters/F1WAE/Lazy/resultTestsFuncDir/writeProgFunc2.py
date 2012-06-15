from random import randrange

def generateProg(nodes):
    if nodes == 0:
        return "0"
    elif nodes == 1:
        return "x"
    else:
        nodes_left = randrange(nodes+1)
        nodes_right = nodes - nodes_left
        left = generateProg(nodes_left)
        right = generateProg(nodes_right)
        return "( + {0} {1} )".format(left,right)

def generateFunc(nodes):
    prog = generateProg(nodes)
    func = "{ (f x) "+prog+ " }"
    return func
    
def buildProg(n, name="progExample"):
    with open(name,"w") as ae:
        ae.write(generateFunc(n)+"\n (f (f 3)) \n")

if __name__ == "__main__":
    import sys
    try:
        if sys.argv[1] == '-i':
            try:
                n=int(sys.argv[3])
            except ValueError:
                print("Wrong argument for nodes")
            buildProg(n, sys.argv[2])
        else:
            while True:
                n=input("Choose the number of nodes of the expression in the function (integer expected):")
                try:
                    n = int(n)
                    break
                except ValueError:
                    continue
            buildProg(n, sys.argv[1])
    except IndexError:
        while True:
            n=input("Choose the number of nodes of the expression in the function (integer expected):")
            try:
                n = int(n)
                break
            except ValueError:
                continue
        buildProg(n)
