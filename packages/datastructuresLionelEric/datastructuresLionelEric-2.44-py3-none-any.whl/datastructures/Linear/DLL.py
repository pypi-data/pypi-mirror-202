import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

class DLL:

    def __init__(self, node=None):
        self.head = node 
        self.size = 1 if node else 0
        self.tail = node #tail pointing to same node as head

    def InsertHead(self, new_node):
        if self.head is None: #if it is empty DLL
            self.head = new_node
            self.tail = new_node
        else: #if there it is not empty
            new_node.prev = None
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def InsertTail(self, new_node):
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = None
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def Insert(self, new_node, position):
        if position < 1 or position > self.size + 1:
            raise ValueError("Invalid position")
        if position == 1:
            self.InsertHead(new_node)
        elif position == self.size + 1:
            self.InsertTail(new_node)
        else: 
            current = self.head
            for _ in range(position - 2):
                current = current.next
            new_node.prev = current
            new_node.next = current.next
            current.next.prev = new_node
            current.next = new_node
            self.size += 1

    def Sort(self):
        if (self.isSorted() == True):
            return
        if self.head is None or self.head.next is None:
            return

        neighbourNode = self.head.next
        while neighbourNode != None:
            keyData = neighbourNode.val
            sorted_node = neighbourNode.prev
            while sorted_node != None and sorted_node.val > keyData:
                sorted_node.next.val = sorted_node.val
                sorted_node = sorted_node.prev
            if sorted_node:
                sorted_node.next.val = keyData
            else:
                self.head.val = keyData
            neighbourNode = neighbourNode.next
    
    def isSorted(self):
        current = self.head
        while current is not None and current.next is not None:
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
            while current.next is not None and current.next.val < node.val:
                current = current.next
            node.next = current.next
            node.prev = current
            current.next.prev = node
            current.next = node
            self.size += 1

    def Search(self, node): 
        current = self.head
        while current is not None:
            if current.val == node.val:
                return current
            current = current.next
        return None

    def DeleteHead(self):
        if self.head is None: #list is empty
            return 
        elif self.head == self.tail: # the list has only one node
            self.head = None
            self.tail = None
            self.size = 0
            return
        else:
            next_node = self.head.next
            next_node.prev = None
            self.head.next = None
            self.head = next_node
            self.size -= 1
        
    def DeleteTail(self):
        if self.head is None: #list is empty
            return 
        elif self.head == self.tail: # the list has only one node
            self.head = None
            self.tail = None
            self.size = 0
            return
        else:
            prev_node = self.tail.prev
            prev_node.next = None
            self.tail.prev = None
            self.tail = prev_node
            self.size -= 1      

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

            if current_node is None:
                # We've reached the end of the list and circled back to the head.
                break

        return count

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
                while current_node is not None:
                    if current_node.val == node.val:
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                        self.size -= 1
                        break
                    current_node = current_node.next
            i += 1

    def Clear(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def Print(self):
        if self.head is None:
            print("List size: 0")
            print("Sorted: Yes")
            print("List content: ")
            return
        current_node = self.head
        print("List size:", self.size)
        print("Sorted:", self.isSorted())
        print(f"List content:", end=" ")
        while current_node is not None:
            print(current_node.val, end=" ")
            current_node = current_node.next
        print()