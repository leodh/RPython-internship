def generateProg(nodes):
    if nodes == 0:
        return "x"
    else:
        son = generateProg(nodes - 1)
        return "(+{} {})".format(son, son)

def generateFunc(nodes,runs):
    prog = generateProg(nodes)
    funcF = "{ (f x) "+prog+ "}"
    funcRun = "{ (run x) (if (= x 0) (f 3) (with (y (f 3)) (run (- x 1)))) }"
    process = "( run "+str(runs)+")"
    fileT = funcF + "\n" + funcRun + "\n" + process
    return fileT
    
def buildProg(n, runs, name):
    with open(name,"w") as ae:
        ae.write(generateFunc(n,runs))

if __name__ == "__main__":
    import sys
    try:
        try:
            n=int(sys.argv[1])
        except ValueError:
            print("Wrong argument for nodes")
        try:
            runs=int(sys.argv[2])
        except ValueError:
            print("Wrong argument for runs")
        name = "linearTest"+str(n)+"runs"+str(runs)
        buildProg(n, runs, name)
        print(name)
    except IndexError:
        print("You must supply number of nodes and runs.")

