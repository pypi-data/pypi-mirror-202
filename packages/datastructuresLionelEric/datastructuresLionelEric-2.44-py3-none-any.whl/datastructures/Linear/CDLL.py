import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from Linear.DLL import DLL

class CDLL(DLL):

    def __init__(self, node=None):
        if node is not None:
            self.head = node
            self.tail = node
            self.head.next = self.tail
            self.head.prev = self.tail
            self.size = 1
        else:
            self.head = None
            self.tail = None
            self.size = 0

    def InsertHead(self, new_node):
        if self.head is None: #if it is empty CDLL
            self.head = new_node
            self.tail = new_node
            self.next = new_node
            self.prev = new_node
        else: 
            new_node.next = self.head 
            new_node.prev = self.tail
            self.head.prev = new_node 
            self.tail.next = new_node
            self.head = new_node
        self.size += 1

    def InsertTail(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.next = new_node
            self.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.head.prev = new_node
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def Insert(self, node, position):
        if position <= 0 or position-1 > self.size:
            raise IndexError("Index out of range")
        if position == 1:
            # Inserting at the beginning
            node.next = self.head
            node.prev = self.tail
            self.head.prev = node
            self.head = node
            self.tail.next = node
        elif position-1 == self.size:
            # Inserting at the end
            node.next = self.head
            node.prev = self.tail
            self.tail.next = node
            self.head.prev = node
            self.tail = node
        else:
            # Inserting at a specific position
            current = self.head
            for i in range(1,position):
                current = current.next
            node.next = current
            node.prev = current.prev
            current.prev.next = node
            current.prev = node
        self.size += 1

    def Sort(self):
        prevNode = self.head
        currNode = self.head.next
        for _ in range(1, self.size):
            key = currNode.val
            while prevNode != self.tail and key < prevNode.val:
                prevNode.next.val = prevNode.val
                prevNode = prevNode.prev
            prevNode.next.val = key
            prevNode = currNode
            currNode = currNode.next

    def isSorted(self):
        current = self.head
        while current.next != self.head:
            if current.val > current.next.val:
                return False
            current = current.next
        return True

    def SortedInsert(self, node):
        if (self.isSorted() != True):
            self.Sort()
        if self.head is None: # The list is empty, so insert the node at the beginning
            self.head = node
            self.tail = node
            self.size += 1
            return
        elif self.head.val >= node.val: # The new node should be inserted at the beginning
            self.InsertHead(node)
            return
        elif self.tail.val <= node.val: # The new node should be inserted at the end
            self.InsertTail(node)
            return
        else:  # Find the proper position to insert the new node
            current = self.head
            while current.next is not self.head and current.next.val < node.val:
                current = current.next
            node.next = current.next
            node.prev = current
            current.next.prev = node
            current.next = node
            self.size += 1


    def Search(self, node):
        current = self.head
        while current.next != self.head:
            if current.val == node.val:
                return current
            current = current.next
        return None
    
    def DeleteHead(self):
        super().DeleteHead()
        self.head.prev = self.tail
        self.tail.next = self.head

    def DeleteTail(self):
        super().DeleteTail()
        self.head.prev = self.tail
        self.tail.next = self.head

    def Delete(self, node):
        i = 0
        node_occurrences = self.count_node_occurrences(node)
        while i < node_occurrences:
            if self.head is None: # empty
                return
            elif node.val == self.head.val: # node to delete is the head node
                self.DeleteHead()
            elif node.val == self.tail.val: # node to delete is the tail node
                self.DeleteTail()
            else:
                current_node = self.head
                while current_node is not self.tail:
                    if current_node.val == node.val:
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                        self.size -= 1
                        break
                    current_node = current_node.next  
            i += 1
                    

    def count_node_occurrences(self,node):
        """
        Counts the number of occurrences of a given node in a circular doubly linked list.

        Args:
        - node: the node to search for in the list.

        Returns:
        - The number of occurrences of the node in the list.
        """

        count = 0
        current_node = self.head

        if current_node is None:
            # The list is empty, so there can be no occurrences of the node.
            return 0

        # Traverse the list from the head node until we reach it again.
        while True:
            if current_node.val == node.val:
                count += 1

            current_node = current_node.next

            if current_node == self.head:
                # We've reached the end of the list and circled back to the head.
                break

        return count

    def Clear(self):
        self.head = None
        self.tail = None
        self.prev = None
        self.next = None
        self.size = 0
    
    def Print(self):
        if self.head is None:
            print("List size: 0")
            print("Sorted: Yes")
            print("List content: ")
            return
        print("List Length:", self.size)
        print("Sorted Status:", self.isSorted())
        if self.head is not None:
            current = self.head
            print("List Content:", end=" ")
            while True:
                print(current.val, end=" ")
                current = current.next
                if current == self.head:
                    break
            print()
        else:
            print("List is empty")