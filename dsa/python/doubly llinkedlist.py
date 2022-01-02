class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        self.previous = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        

    # O(1)
    def insert(self,data):
        new_node = Node(data)
        #when list is empty
        if self.head is None:
            self.head=new_node
            self.tail=new_node
        #if there is atleast one item in the linked list
        else:
            new_node.previous=self.tail
            self.tail.next = new_node
            self.tail=new_node

    def traverse_forward(self):
        actual_node = self.head
        while actual_node is not None:
            print(actual_node.data)
            actual_node = actual_node.next

    def traverse_backward(self):
        actual_node = self.tail
        while actual_node is not None:
            print(actual_node.data)
            actual_node = actual_node.previous


if __name__ == "__main__":
    linked_list = DoublyLinkedList()
    linked_list.insert(1)
    linked_list.insert(2)
    linked_list.insert(3)
    linked_list.traverse_forward()
    linked_list.traverse_backward()






        
        
