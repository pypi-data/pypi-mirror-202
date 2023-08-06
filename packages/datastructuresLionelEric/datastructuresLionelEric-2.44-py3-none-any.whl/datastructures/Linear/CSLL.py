import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))


from Nodes.DNode import DNode
from Linear.SLL import SLL

class CSLL(SLL):


    def __init__(self,node =None):
        if node is not None:
            self.head = node
            self.tail = node
            self.head.next = self.tail
            self.size = 1
        else:
            self.head = None
            self.tail = None
            self.size = 0

    def is_Sorted(self):
        """Check if the circular linked list is sorted in non-descending order."""
        if self.size <= 1:
            self.sorted = True
            return
        
        curr = self.head
        while curr.next != self.head:
            if curr.val > curr.next.val:
                self.sorted = False
                return
            curr = curr.next
            
        # Check the last element with the first element

        self.sorted = True

    def InsertTail(self, node):
        if self.head is None:
            self.head = node
            node.next = self.head
            self.tail = node
        else:
            self.tail.next = node
            node.next = self.head
            self.tail = node
        self.size += 1

    def InsertHead(self, node):
        if self.head is None:
            self.head = node
            node.next = self.head
            self.tail = node
        else:
            curr = self.head
            while curr.next != self.head:
                curr = curr.next
            curr.next = node
            node.next = self.head
            self.head = node
        self.size += 1

    def Insert(self, node, position):
        if position <= 0 or position-1 > self.size:
            raise IndexError("Index out of range")
        if position == 1:
            # Inserting at the beginning
            node.next = self.head
            self.head = node
            self.tail.next = node
        elif position-1 == self.size:
            # Inserting at the end
            node.next = self.head
            self.tail.next = node
            self.tail = node
        else:
            # Inserting at a specific position
            curr_node = self.head
            for i in range(1, position - 1):
                curr_node = curr_node.next
            node.next = curr_node.next
            curr_node.next = node
        self.size += 1

    def Search(self, node):
        current = self.head
        while current.next != self.head:
            if current.val == node.val:
                return current
            current = current.next
        return None
    
    
    def DeleteTail(self):
        """Delete the tail node of the circular linked list."""
        if not self.head:
            # If the list is empty, there's nothing to delete
            return

        # Find the last node and the second-to-last node in the list
        last_node = self.head
        second_to_last_node = None
        while last_node.next != self.head:
            second_to_last_node = last_node
            last_node = last_node.next

        # If there is only one node in the list, delete it
        if last_node == self.head:
            self.head = None

        # Otherwise, delete the last node and update the second-to-last node's `next` pointer
        else:
            second_to_last_node.next = self.head
            last_node.next = None
        self.size -=1

    def DeleteHead(self):
        """Delete the head node of the circular linked list."""
        if not self.head:
            # If the list is empty, there's nothing to delete
            return

        # Find the last node in the list
        last_node = self.head
        while last_node.next != self.head:
            last_node = last_node.next

        # If there is only one node in the list, delete it
        if last_node == self.head:
            self.head = None

        # Otherwise, delete the head node and update the last node's `next` pointer
        else:
            second_node = self.head.next
            self.head.next = None
            self.head = second_node
            last_node.next = second_node
        self.size -=1

    def Delete(self, node):
        i = 0
        node_occurrences = self.count_node_occurrences(node)
        while i < node_occurrences:
            if self.head is None: # empty
                return
            elif self.head.val == node.val: # node to delete is the head node
                self.DeleteHead()
            else:
                current_node = self.head
                while current_node.next != self.head:
                    if current_node.next.val == node.val:
                        current_node.next = current_node.next.next
                        self.size -= 1
                        break
                    current_node = current_node.next 
            i += 1

    def Sort(self):
        sort = self.is_Sorted()
        if not self.head or not self.head.next or sort == True:
            return

        if self.size > 1:
            for i in range(self.size-1):
                currNode = self.head
                for j in range(self.size-i-1):
                    if currNode.val > currNode.next.val:
                        temp = currNode.val
                        currNode.val = currNode.next.val
                        currNode.next.val = temp
                    currNode = currNode.next

    def Clear(self):
        """Delete the entire circular linked list."""
        if not self.head:
            # If the list is empty, there's nothing to delete
            return

        # Find the last node in the list
        last_node = self.head
        while last_node.next != self.head:
            last_node = last_node.next

        # Delete all nodes in the list
        current_node = self.head
        while current_node != last_node:
            next_node = current_node.next
            current_node.next = None
            current_node = next_node
        last_node.next = None

        # Update head pointer to indicate the list is empty
        self.head = None

    def Print(self):
        """Print the circular linked list information on the screen."""

        if self.head is None:
            print("List size: 0")
            print("Sorted: Yes")
            print("List content: ")
            return

        # Print the list length
        print("List size:", self.size)
        self.is_Sorted()

        # Print the sorted status
        print("Sorted: " + ("Yes" if self.sorted else "No"))

        # Print the list content
        if not self.head:
            print("List is empty")
        else:
            current_node = self.head
            print("List content:", end=" ")
            while True:
                print(current_node.val, end=" ")
                current_node = current_node.next
                if current_node == self.head:
                    break
            print()

    def SortedInsert(self, node):
        if (self.is_Sorted() != True):
            self.Sort()
        if self.head is None: # The list is empty, so insert the node at the beginning
            self.head = node
            self.tail = node
            node.next = self.head
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
            current.next = node
            self.size += 1
    
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