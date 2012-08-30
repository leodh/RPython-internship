from random import randrange

def generateProg(nodes):
    if nodes == 0:
        return "x"
    else:
        right = generateProg(nodes - 1)
        return "{+ %s %s}" % (right,right)

def generateFunc(nodes,runs):
    prog = generateProg(nodes)
    funcF = "{ fun {x} %s}" % prog
    fileT = """{
        {fun {f}
         { rec
           {run { fun {x}
                  {if0 x {f 5} {{fun {y} {run {- x 1}}} {f 5}} }
                }
           } {run %s}
         } }
        %s}""" % (str(runs), funcF)
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
        name = "test"+str(n)+"runs"+str(runs)
        buildProg(n, runs, name)
        print(name)
    except IndexError:
        print("You must supply number of nodes and runs.")
