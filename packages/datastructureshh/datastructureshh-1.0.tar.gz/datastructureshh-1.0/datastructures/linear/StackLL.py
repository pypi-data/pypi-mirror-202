from datastructures.nodes.DNode import Node
from datastructures.linear.SLL import SinglyLinkedList

class StackLL:

    def __init__(self, init_value = None):
        list = SinglyLinkedList(init_value)
        self.head = list.head
        self.tail = list.tail
        self.size = list.size

    def Push(self, value):
        SinglyLinkedList.InsertHead(self, value)
    
    def Pop(self):
        SinglyLinkedList.DeleteHead(self)
    
    def Search(self, value):
        found_val = SinglyLinkedList.Search(self, value)
        return found_val

    def IsSorted(self):
        sorted = SinglyLinkedList.IsSorted(self)
        return sorted

    def Clear(self):
        SinglyLinkedList.Clear(self)
    
    def Print(self):
        SinglyLinkedList.Print(self)
