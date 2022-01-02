class Node:
    def __init__(self,data):
        self.data = data
        self.nextNode = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.numOfNodes = 0

    # O(1)
    def insert_start(self,data):
        self.numOfNodes +=  1
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            new_node.nextNode = self.head
            self.head = new_node

    # O(n)
    def insert_end(self,data):
        self.numOfNodes += 1
        new_node = Node(data)
        actual_node = self.head
        while actual_node.nextNode is not None:
            actual_node = actual_node.nextNode

        actual_node.nextNode = new_node

    # O(n)
    # we keep two pointers, one with 1 step and another with 2 steps.By the time, second pointer reaches end, first one will be at middle.
    def get_middle_node(self):
        fast_pointer = self.head
        slow_pointer = self.head
        while fast_pointer.nextNode and fast_pointer.nextNode.nextNode:
            fast_pointer = fast_pointer.nextNode.nextNode
            slow_pointer = slow_pointer.nextNode
        return  slow_pointer

    def remove(self,data):
        if self.head is None:
            return

        actual_node = self.head
        previous_node = None
        while actual_node is not None and actual_node.data != data:
            previous_node = actual_node
            actual_node = actual_node.nextNode

        # item not present in linked list
        if actual_node is None:
            return

        self.numOfNodes -= 1
        # it means found the data as first element.
        if previous_node is None:
            self.head = actual_node.nextNode
        else:
            previous_node.nextNode = actual_node.nextNode

    #O(1)
    def size_of_list(self):
        return self.numOfNodes

    def traverse(self):
        actual_node = self.head
        while actual_node is not None:
            print(actual_node.data)
            actual_node = actual_node.nextNode

    def reverse(self):
        current_node = self.head
        previous_node = None
        next_node = None

        while current_node is not None:
            next_node = current_node.next_node
            current_node.next_node = previous_node
            previous_node = current_node
            current_node = next_node
        self.head = previous_node


linked_list = LinkedList()
linked_list.insert_start(4)
linked_list.insert_start(3.0)
linked_list.insert_start('Adam')
linked_list.insert_end(10)
linked_list.insert_end(100)
linked_list.insert_end(1000)
linked_list.traverse()
print("size of linked list %d " % linked_list.size_of_list())
linked_list.remove(10)
linked_list.remove(300)
linked_list.remove('Adam')
linked_list.traverse()
print("size of linked list %d " % linked_list.size_of_list())

print(linked_list.get_middle_node().data)

linked_list.reverse()
linked_list.traverse()

        
        
