from random import randrange

def generateProg(depth):
    if depth == 0:
        return "{0}".format(randrange(10))
    else:
        side = randrange(2)
        light_side_depth = randrange(depth)
        light_side = generateProg(light_side_depth)
        loud_side = generateProg(depth -1)
        sign = randrange(2)
        if side == 0:#loud son on the left
            left = loud_side
            right = light_side
        else: #loud son on the right
            left = light_side
            right = loud_side
        if sign == 0: #Addition
            return "(with (l {0}) (with (r {1}) ( + l r )))".format(left, right)
        else:
            return "(with (l {0}) (with (r {1}) ( - l r )))".format(left, right)

def buildProg(n, name="progExample"):
    with open(name,"w") as ae:
        ae.write(generateProg(n))

if __name__ == "__main__":
    import sys
    try:
        if sys.argv[1] == '-i':
            try:
                n=int(sys.argv[3])
            except ValueError:
                print("Wrong argument for depth")
            buildProg(n, sys.argv[2])
        else:
            while True:
                n=input("Choose the depth of the expression (integer expected):")
                try:
                    n = int(n)
                    break
                except ValueError:
                    continue
            buildProg(n, sys.argv[1])
    except IndexError:
        while True:
            n=input("Choose the depth of the expression (integer expected):")
            try:
                n = int(n)
                break
            except ValueError:
                continue
        buildProg(n)
