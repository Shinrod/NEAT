# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------
from math import e
from copy import copy

# --------------------------------------------------------------------------------------------------------

def sigmoid(x):
    ''' Activation function '''
    return 1/(1+ e**-(4.9*x))

# --------------------------------------------------------------------------------------------------------
class Node:
    
# --------------------------------------------------------------------------------------------------------

    def __init__(self, number, layer):
        ''' Make a Node '''
        self.number = number
        self.layer = layer
        self.input = 0
        self.value = 0
        
# --------------------------------------------------------------------------------------------------------

    def __repr__(self):
        ''' Define how it is represented when logged in the console '''
        text = '<Node {} - layer {}>'.format(self.number, self.layer)
        return text

# --------------------------------------------------------------------------------------------------------

    def __eq__(self, other):
        ''' Define what it means for two nodes to be equal '''
        areEqual = self.number == other.number
        return areEqual
    
# --------------------------------------------------------------------------------------------------------

    def use(self):
        ''' Use the node '''
        try :
            self.value = sigmoid(self.input)
        except OverflowError as e:
            print(self.input)
            print(self.number)
            print(self.layer)
            raise e
        # Reset the input
        self.input = 0
        
# --------------------------------------------------------------------------------------------------------

    def __copy__(self):
        ''' Copy the node '''
        new = Node(self.number, self.layer)
        new.number = copy(self.number)
        new.layer = copy(self.layer)
        new.input = 0
        new.value = 0
        return new