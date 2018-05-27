# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------
from copy import deepcopy
# --------------------------------------------------------------------------------------------------------
class PieceOfHistory:

# --------------------------------------------------------------------------------------------------------

    def __init__(self, start, end, innovationNumber, previousInnovations):
        ''' Store this new piece of history ! (i.e. this new innovation that never occured like that before) '''
        self.start = start
        self.end = end
        self.innovationNumber = innovationNumber
        self.previousInnovations = deepcopy(previousInnovations)

# --------------------------------------------------------------------------------------------------------

    def __repr__(self):
        ''' Define how it is logged in the console '''
        text = '<Innovation {} from {} to {}>'.format(self.innovationNumber, self.start, self.end)
        return text
      
# --------------------------------------------------------------------------------------------------------

    def matches(self, genome, start, end):
        ''' Tell if 2 innovations are the same '''
#        print('Testing {} to {}'.format(start, end))
#        print('{} to {} exists'.format(self.start, self.end))
        if self.start != start:
#            print('Not the same start')
            return False
        if self.end != end:
#            print('Not the same end')
            return False
        for connection in genome.connections:
            if connection.innovationNumber not in self.previousInnovations:
                return False
        # If it passes all the trials, it is the same !
        return True