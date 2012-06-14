class Node:
    """General class for nodes of AST"""
    
class InsideNode(Node):
    """class for inside node with two sons"""

    def __init__(self, op, leftSon, rightSon):
        self.leftSon = leftSon
        self.rightSon = rightSon
        self.op = op


class Leaf(Node):
    """class for leafs"""

    def __init__(self,n):
        self.value = n



    
