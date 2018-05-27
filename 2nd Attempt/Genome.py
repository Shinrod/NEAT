# -*- coding: utf-8 -*-
from Node import Node
from Connection import Connection
from InnovationHistory import PieceOfHistory
import numpy as np
from graphviz import Digraph
from copy import copy

# --------------------------------------------------------------------------------------------------------
class Genome:
    
    def __init__(self, inputs, outputs):
        ''' Make a brain for the player to use '''
        self.input = inputs
        self.output = outputs
        self.nodes = []
        self.connections = []
        
        # Create the input nodes
        for i in range(self.input):
            node = Node(len(self.nodes), layer = 0)
            self.addNode(node)
        
        # Add a bias node
        self.biasNode = Node(len(self.nodes), layer = 0)
        self.addNode(self.biasNode)
        
        # Add the ouput nodes
        for i in range(self.output):
            node = Node(len(self.nodes), layer = 1)
            self.addNode(node)
        
        self.nbOfLayers = 2
        self.updateLayers()
            
# --------------------------------------------------------------------------------------------------------

    def addNode(self, node):
        ''' Simple stuff '''
        self.nodes.append(node)

# --------------------------------------------------------------------------------------------------------

    def addConnection(self, connection):
        ''' Simple stuff '''
        self.connections.append(connection)

# --------------------------------------------------------------------------------------------------------

    def updateLayers(self):
        ''' Put all the nodes in the layer they belong to '''
#        try:
        self.layers = [[] for i in range(self.nbOfLayers)]
        for node in self.nodes:
            self.layers[node.layer].append(node)
#        except IndexError as e:
#            for node in self.nodes:
#                print(node)
#            print('Nodes : ', self.nodes)
#            print('nbOfLayers : ', self.nbOfLayers)
#            print('layers :', self.layers)
#            raise e

# --------------------------------------------------------------------------------------------------------

    def getNextNodeNumber(self):
        ''' The number of the next node is the length of the node list '''
        return len(self.nodes)

# --------------------------------------------------------------------------------------------------------

    def crossover(self, other):
        ''' Cross the two brains over
            The player controled by self must be fittest that the one controlled by other
        '''
        child = Genome(self.input, self.output)
        
        # The child has the same nodes as it's first parent
        child.nodes = []
        child.connections = []
        for node in self.nodes:
            child.addNode(copy(node))
        child.biasNode = copy(self.biasNode)
        child.layers = self.layers
        child.nbOfLayers = self.nbOfLayers
        
        # Add the connections to the child's brain
        for connection1 in self.connections:
            # Check if the connection is the same gene than one in the other
            matching = False
            for connection2 in other.connections:
                # Matching genes
                if connection1.innovationNumber == connection2.innovationNumber:
                    # Pick a random one
                    if np.random.rand() < 0.5:
                        connection = copy(connection1)
                    else:
                        connection = copy(connection2)
                    # If the connection is disabled in one of the two parents...
                    if (not connection1.enabled) or (not connection2.enabled):
                        # ...  the child one has 75% chances to be disabled 
                        if np.random.rand() < 0.75:
                            connection.disable()
                        else:
                            connection.enabled = True
                    matching = True
                    break
            if not matching:
                connection = copy(connection1)
            child.addConnection(connection)
        child.updateLayers()
        return child
                
# --------------------------------------------------------------------------------------------------------

    def mutate(self, innovationHistory):
        ''' Mutate the network
            There are 3 mutations possible :
                - Weight mutation
                - Connection mutation
                - Node mutation
        '''
        # Weight mutation
        if np.random.rand() < 0.80:
            for connection in self.connections:
                connection.mutate()
        
        # Connection mutation
        if np.random.rand() < 0.05:
            self.connectionMutation(innovationHistory)
            
        # Node mutation
        if np.random.rand() < 0.03:
            self.nodeMutation(innovationHistory)
            
# --------------------------------------------------------------------------------------------------------

    def connectionMutation(self, innovationHistory):
        ''' Add a connection to the network '''
        # If the network is fully connected, we can't add a connection
        if self.fullyConnected():
            return None
        # Pick 2 nodes that are not connected to each other
        node1, node2 = np.random.choice(self.nodes, (2,), replace = False)
        while self.areConnected(node1, node2) or node1.layer == node2.layer:
            node1, node2 = np.random.choice(self.nodes, (2,), replace = False)
        if node1.layer > node2.layer:
            node1, node2 = node2, node1
        # Get the innovation number : If the innovation already occured in the population, we want both to have the same number
        innovationNumber = self.getInnovationNumber(node1, node2, innovationHistory)
        # Get a weight between -1 & 1
        weight = 2*np.random.rand()-1
        # Make the new connection
        connection = Connection(node1, node2, weight, innovationNumber)
        self.addConnection(connection)
                                
# --------------------------------------------------------------------------------------------------------

    def nodeMutation(self, innovationHistory):
        ''' Add a node to the network
            We pick a connection and insert a node in between
        '''
        # Pick a connection
        # If there is no connection, make one
        if len(self.connections) == 0:
            self.connectionMutation(innovationHistory)
            return None
        oldConnection = np.random.choice(self.connections)
        i = 0
        while not oldConnection.enabled:
            i+= 1
            try:
                oldConnection = copy(np.random.choice(self.connections))
                assert i < 300
            except AssertionError as e:
                print(self.connections)
                print(len(self.connections))
                self.draw()
                for connection in self.connections:
                    print(connection.enabled)
                raise e
        oldConnection.disable()
#        print('Old connection :', oldConnection)
        # Make a node and add it to the network
        newNode = Node(self.getNextNodeNumber(), self.nodes[oldConnection.start.number].layer+1)
        self.addNode(newNode)
        # Make 2 connections to 'hold' that node
        innovationNuber = self.getInnovationNumber(oldConnection.start, newNode, innovationHistory)
        weight = 1
        newConnection1 = Connection(oldConnection.start, newNode, weight, innovationNuber)
#        print('newConnection1 :', newConnection1)
        self.addConnection(newConnection1)
        # The 2nd one
        innovationNuber = self.getInnovationNumber(newNode, oldConnection.end, innovationHistory)
        weight = oldConnection.weight
        newConnection2 = Connection(newNode, oldConnection.end, weight, innovationNuber)
#        print('newConnection2 :', newConnection2)
        self.addConnection(newConnection2)
        # Shift the layers so that the new node is not connected to a node in the same layer
        if newNode.layer == self.nodes[oldConnection.end.number].layer:
            for numLayer in range(len(self.layers)):
                if numLayer >= newNode.layer:
                    for node in self.layers[numLayer]:
                        if node != newNode:
                            node.layer += 1
            self.nbOfLayers += 1 
        # Don't forget to update the layers
#        try:
        self.updateLayers()
#        except:
#            print(newNode.layer)
#            print(newNode)
#            print(self.nbOfLayers)
#            print(self.connections)
#            raise 'Error'
            
# --------------------------------------------------------------------------------------------------------

    def fullyConnected(self):
        ''' Check if the network is fully connected
            Basically count how many connections are possible and check if we have that number of connections
        '''
        self.updateLayers()
        # Count the max number of connections
        maxConnections = 0
        for numLayer in range(len(self.layers)-1):
            for numLayer2 in range(numLayer+1, len(self.layers)):
                maxConnections += len(self.layers[numLayer]) * len(self.layers[numLayer2])
        if len(self.connections) != maxConnections:
            return False
        else:
            return True
        
# --------------------------------------------------------------------------------------------------------

    def areConnected(self, node1, node2):
        ''' Tell if two nodes are connected '''
        # Swap the two if needed to have them in order
        if node1.layer > node2.layer:
            node1, node2 = node2, node1
        # Go through all the connections to check if they are connected
        for connection in self.connections:
            if connection.start == node1 and connection.end == node2:
                return True
        return False
        
# --------------------------------------------------------------------------------------------------------

    def getInnovationNumber(self, start, end, innovationHistory):
        ''' Make sure that 2 innovations that are the same have the same innovation number '''
        # Check if the innovation already occured
        isNew = True
        for innovation in innovationHistory:
            if innovation.matches(self, start, end):
                isNew = False
                innovationNumber = innovation.innovationNumber
                break
        if isNew:
            # Get a new number
            innovationNumber = len(innovationHistory)
            previousInnovations = []
            for connection in self.connections:
                previousInnovations.append(connection.innovationNumber)
            innovationHistory.append(PieceOfHistory(start, end, innovationNumber, previousInnovations))
        return innovationNumber

# --------------------------------------------------------------------------------------------------------

    def feedForward(self, inputs):
        ''' Use the brain ! '''
        self.updateLayers()
        # The input of the input neurons are 'inputs'
        for i, node in enumerate(self.layers[0]):
            if node != self.biasNode:
                node.input = inputs[i]
        # The bias has an input of 1
        self.biasNode.input = 1
        
        # Update the network to know which nodes are connected to which
        nodesConnections = self.getNodesConnections()
        for node in self.layers[0]:
            for connection in nodesConnections[node.number]:
                if connection.enabled:
                    connection.end.input += node.value * connection.weight
        # Use the nodes
        outputs = []
        for numLayer in range(1, len(self.layers)):
            for node in self.layers[numLayer]:
                node.use()
                for connection in nodesConnections[node.number]:
                    if connection.enabled:
                        connection.end.input += node.value * connection.weight
                if numLayer == len(self.layers)-1:
                    outputs.append(node.value)
        return outputs                
                
# --------------------------------------------------------------------------------------------------------

    def getNodesConnections(self):
        ''' Return the list of the connections that are leaving each node '''
        nodesConnections = [[] for i in range(len(self.nodes))]
        for connection in self.connections:
            nodesConnections[connection.start.number].append(connection)
        return nodesConnections        
        
# --------------------------------------------------------------------------------------------------------

    def __copy__(self):
        ''' Return a copy of the genome '''
        new = Genome(self.input, self.output)
        new.connections = []
        new.nodes = []
        for node in self.nodes:
            new.addNode(copy(node))
        for connection in self.connections:
            new.addConnection(copy(connection))
        new.biasNode = copy(self.biasNode)
        new.layers = self.layers
        new.nbOfLayers = self.nbOfLayers
        new.updateLayers()
        return new
        
# --------------------------------------------------------------------------------------------------------
 
    def draw(self):
        ''' Draw the network '''
        # Have a graph
        graph = Digraph('Network', format='svg')
        # Make it go from left to the right
        graph.attr(rankdir = 'LR')
        # Sort nodes per layer
        self.updateLayers()
        # Make sure the nodes appear in layer
        for numLayer in range(len(self.layers)):
            for i, node in enumerate(self.layers[numLayer]):
                # Give color to the nodes
                if node.layer == 0:
                    # Input : yellow
                    color = "0.166 1 0.5"
                elif node.layer == len(self.layers)-1:
                    # Output : blue
                    color = "0.66 1 0.5"
                else:
                    # Hidden : black
                    color = "0.528 1 0.5"
                graph.node(str(node.number), color = color, shape = 'circle')
                # Be sure that the nodes are sorted in order
                # It's kinda tricky but it does the job
                if i !=0:
                    # Make some invisible edges that are ordring the nodes
                    graph.edge(str(self.layers[numLayer][i-1].number), str(node.number), style = 'invis')
            # Part of the 'ordering nodes' thing (re-align the nodes in the same layer)
            if len(self.layers[numLayer]) > 1 :
                nodes = ''
                for node in self.layers[numLayer]:
                    nodes += str(node.number) + ' '
                # Here we write some raw graphviz text because I don't think we can do this with only python commands
                graph.body.append('\t{rank = same; ' + nodes + '; rankdir=LR;}\n\t')
            # Order the layers
            if numLayer > 0:
                graph.edge(str(self.layers[numLayer-1][0].number), str(self.layers[numLayer][0].number), style = 'invis')
                
        # Draw the connections
        for connection in self.connections:
            # Only draw the enabled ones
            if connection.enabled and connection.weight != 0:
#            if connection.enabled:
                # Make some fancy colors based on weight
                if connection.weight < 0:
                    color = "0 " + str(-connection.weight) + " 0.5"
                else:
                    color = "0.3333 " + str(connection.weight) + " 0.5"
                graph.edge(str(connection.start.number), str(connection.end.number), color = color, label = str(connection.innovationNumber), edgetooltip = str(connection.weight))
        # Finally, draw it !
        graph.render(view = True)
        return graph
            