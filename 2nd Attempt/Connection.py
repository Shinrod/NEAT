# -*- coding: utf-8 -*-
import numpy as np

# --------------------------------------------------------------------------------------------------------
class Connection:

# --------------------------------------------------------------------------------------------------------

    def __init__(self, start, end, weight, innovationNumber):
        ''' Defines a connection between two nodes
            start is the node from which the connection come
            end -------------- to ---------------------- go
        '''
        self.start = start
        self.end = end
        self.weight = weight
        self.innovationNumber = innovationNumber
        self.enabled = True

# --------------------------------------------------------------------------------------------------------

    def __repr__(self):
        ''' Defines how it's shown in the console '''
        text = '<Connection {} from {} to {}>'.format(self.innovationNumber, self.start, self.end)
        return text

# --------------------------------------------------------------------------------------------------------

    def mutate(self):
        ''' Mutate the connection '''
        # In 90% cases, give the weights a little nudge
        if np.random.rand() < 0.9:
            self.weight += np.random.normal()/50
            # Be sure self.weight is between -1 & 1
            if self.weight > 1:
                self.weight = 1
            elif self.weight < -1:
                self.weight = -1
        else:
            # Assign a new value
            self.weight = 2*np.random.rand() - 1

# --------------------------------------------------------------------------------------------------------

    def disable(self):
        ''' Simple stuff '''
        self.enabled = False

# --------------------------------------------------------------------------------------------------------

    def __copy__(self):
        ''' Use copy(connection) or connection.__copy__() to clone the connection '''
        new = Connection(self.start, self.end, self.weight, self.innovationNumber)
        new.enabled = self.enabled
        return new