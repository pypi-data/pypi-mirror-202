import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))


from nodes.TNode import TNode
from BST import BST
from AVL import AVL

def testBST():
    testTree = BST()
    testNode = TNode(6)
    testTree.Insert(testNode)
    testTree.Insert(4)
    testTree.Insert(9)
    print("Testing Breadth First Search after inserting the values 6, 4, and 9:")
    testTree.printBF()
    print("Testing  printInOrder:")
    testTree.printInOrder()
    testTree.Insert(2)
    testTree.Insert(5)
    testTree.Insert(7)
    testTree.Insert(11)
    testTree.Insert(1)
    testTree.Insert(3)
    print("Testing delete for the value 5")
    testTree.delete(5)
    print("Testing printBF after inserting 2,5,7,11,1,3 and deleting 5")
    testTree.printBF()

    print("Testing search on the value 9")
    if(testTree.search(9)):
        print("Search function for the value 9  was successful")
    else:
        print("Search function for the value 9  was unsuccessful")


    
    
    print()


    #[x for x in test.breadth_first(root)] #tests printBF

def testTnode():
    test = TNode()
    print("Setting data to 10 and balance to 1")
    test.set_data(10)
    test.set_balance(1)
    left = TNode(6)
    right = TNode(15)
    parent = TNode(20)
    test.set_left(left)
    print("Setting left node to " + str(left.get_data()))
    test.set_right(right)
    print("Setting right node to " + str(right.get_data()))
    test.set_parent(parent)
    print("Setting parent node to " + str(parent.get_data()))
    print("Data of testNode: " + str(test.get_data()))
    print("Balance of testNode: " + str(test.get_balance()))
    print("Left Node data: ")
    test.get_left().print()
    print("Right Node data: ")
    test.get_right().print()
    print("Parent Node data: ")
    test.get_parent().print()


def testBST2():
        testTree = BST()
        testNode = TNode(2)
        testTree.Insert(testNode)
        testTree.Insert(5)
        testTree.Insert(0)
        testTree.Insert(7)
        testTree.Insert(6)


        print("Testing Breadth First Search after inserting the values 6, 4, and 9:")
        testTree.printBF()


def testAVL():
        testTree = AVL()
        testNode = TNode(2)
        testTree.Insert(testNode)
        testTree.Insert(5)
        testTree.Insert(0)
        testTree.Insert(7)
        testTree.Insert(6)

        print("Testing Breadth First Search after inserting the values 2, 5, 0, 7, and 6:")
        testTree.printBF()
        testTree.balance_avl()
        print("Testing Breadth First Search after balancing")

        testTree.printBF()









if __name__ == "__main__":

    # print("Testing BST \n")
    # testBST()
    # print("Testing TNode \n")
    # testTnode()
   #print("Testing AVL \n")
 
   testAVL()

