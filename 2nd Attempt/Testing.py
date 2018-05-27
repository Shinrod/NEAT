# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------
''' XOR Test '''
from Population import Population
from Connection import Connection
import numpy as np
import matplotlib.pyplot as plt

p = Population(150)
for player in p.people:
    weight = 2*np.random.rand() -1
    node1 = player.brain.nodes[0]
    node2 = player.brain.nodes[-1]
    innovationNumber = player.brain.getInnovationNumber(node1, node2 , p.innovationHistory)
    connection = Connection(node1, node2, weight, innovationNumber)
    player.brain.addConnection(connection)

    weight = 2*np.random.rand()-1
    node1 = player.brain.nodes[1]
    node2 = player.brain.nodes[-1]
    innovationNumber = player.brain.getInnovationNumber(node1, node2 , p.innovationHistory)
    connection = Connection(node1, node2, weight, innovationNumber)
    player.brain.addConnection(connection)

    weight = 2*np.random.rand()-1
    node1 = player.brain.nodes[2]
    node2 = player.brain.nodes[-1]
    innovationNumber = player.brain.getInnovationNumber(node1, node2 , p.innovationHistory)
    connection = Connection(node1, node2, weight, innovationNumber)
    player.brain.addConnection(connection)

maxScore = 0
while maxScore < 4 and p.gen > 50:
    p.updateAlive()
    for player in p.people:
        if player.score > maxScore:
            maxScore = player.score
    p.naturalSelection()
    print(p.gen)
p.updateAlive()
p.prepare()
p.best.brain.draw()

fig = plt.figure()
ax = fig.add_subplot(111)

fit = []
for player in p.bests:
    fit.append(player.fitness)
x = range(len(p.bests))
line, = ax.plot(x,fit, color = 'red', label = 'Max fitness')


average = []
for av in p.average:
    average.append(av)
line2, = ax.plot(x, average, color = 'green', label = 'average')
ax.legend()
ax.set_title('Fitness')
plt.show(fig)


# --------------------------------------------------------------------------------------------------------
''' Feed forward test '''
#from Population import Population
#
#p = Population(20)
#inputs = [0.5, 0.2]
#for player in p.people:
#    print(player.think(inputs))





# --------------------------------------------------------------------------------------------------------
''' Count gene and species recognition '''
#from Population import Population
#from Species import Species
#import time
#
#p = Population(20)
#for player in p.people[:5]:
#    player.brain.connectionMutation(p.innovationHistory)
#    player.brain.connectionMutation(p.innovationHistory)
#    player.brain.connectionMutation(p.innovationHistory)
#    player.brain.nodeMutation(p.innovationHistory)
#    player.brain.connectionMutation(p.innovationHistory)
#    player.brain.draw()
#    time.sleep(1)
#
#p.evaluate()
#s = Species(p.people[0])
#for player in p.people[:5]:
#    print(s.sameSpecies(player))



# --------------------------------------------------------------------------------------------------------
''' Exemple of why connections that are connected to the two same nodes should have the same innovation number '''
#from Population import Population
#from Connection import Connection
#import time
#
#p = Population(10)
#player = p.people[0]
#node1 = player.brain.nodes[0]
#node2 = player.brain.nodes[3]
#weight = -0.8
#connection = Connection(node1, node2, weight, player.brain.getInnovationNumber(node1, node2, p.innovationHistory))
#player.brain.addConnection(connection)
#player.brain.nodeMutation(p.innovationHistory)
#node1 = player.brain.nodes[2]
#node2 = player.brain.nodes[4]
#weight = 0.8
#connection = Connection(node1, node2, weight, player.brain.getInnovationNumber(node1, node2, p.innovationHistory))
#player.brain.addConnection(connection)
#player.brain.draw()
#time.sleep(2)
#
#player2 = p.people[1]
#node1 = player2.brain.nodes[2]
#node2 = player2.brain.nodes[4]
#weight = 0.3
#connection = Connection(node1, node2, weight, player2.brain.getInnovationNumber(node1, node2, p.innovationHistory))
#player2.brain.addConnection(connection)
#player2.brain.draw()





# --------------------------------------------------------------------------------------------------------
''' Innovation testing '''
#from Population import Population
#
#p = Population(20)
#print(p.innovationHistory)
#for player in p.people:
#    player.brain.connectionMutation(p.innovationHistory)
#    print()
##    print(p.innovationHistory)
