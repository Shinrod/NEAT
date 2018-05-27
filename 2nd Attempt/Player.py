# -*- coding: utf-8 -*-
'''
The Player class that is used by NEAT

All what is marked with "TODO : Fill here" are some game dependant stuff
'''
# --------------------------------------------------------------------------------------------------------
from Genome import Genome
from copy import copy

# --------------------------------------------------------------------------------------------------------
class Player:

    brainInput = 2 # TODO : Fill here
    brainOutput = 1 # TODO : Fill here

# --------------------------------------------------------------------------------------------------------

    def __init__(self):
        ''' Make a new player '''
        self.brain = Genome(self.brainInput, self.brainOutput)
        self.fitness = 0
        self.alive = True
        self.score = 0

# --------------------------------------------------------------------------------------------------------

    def look(self):
        ''' Set the inputs '''
        # TODO : Fill here
        return inputs

# --------------------------------------------------------------------------------------------------------

    def think(self, inputs):
        ''' Use the brain '''
        outputs = self.brain.feedForward(inputs)
        return outputs

# --------------------------------------------------------------------------------------------------------

    def act(self, outputs):
        ''' Act according to what the brain said '''
        # TODO : Fill here


# --------------------------------------------------------------------------------------------------------

    def update(self):
        ''' Make the brain play '''
        self.distance = 0
        self.score = 0
        inputs = [0,0]
        outputs = self.think(inputs)
        self.distance += abs(outputs[0] - 0)
        self.score += int(outputs[0] < 0.5)
        inputs = [0,1]
        outputs = self.think(inputs)
        self.distance += abs(outputs[0] - 1)
        self.score += int(outputs[0] >= 0.5)
        inputs = [1,0]
        outputs = self.think(inputs)
        self.distance += abs(outputs[0] - 1)
        self.score += int(outputs[0] >= 0.5)
        inputs = [1,1]
        outputs = self.think(inputs)
        self.distance += abs(outputs[0] - 0)
        self.score += int(outputs[0] < 0.5)
#        print(self.score)
        # TODO : Fill here if needed

# --------------------------------------------------------------------------------------------------------

    def evaluate(self):
        ''' Update the fitness of the player '''
        # TODO : Fill here
        # Something about 'self.fitness = ...'
        self.fitness = (4 - self.distance)**2

# --------------------------------------------------------------------------------------------------------

    def __copy__(self):
        ''' Copy the player '''
        new = Player()
        new.brain = copy(self.brain)
        new.fitness = self.fitness
        return new