# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------
import numpy as np
from copy import copy

# --------------------------------------------------------------------------------------------------------
class Species:
    
    coefDisjoint = 1
    coefExcess = 1
    coefWeight = 0.4
    
    distanceTreshold = 3
    
# -------------------------------------------------------------------------------------------------------- 
    
    def __init__(self, player):
        ''' Make a new species '''
        self.people = [player]
        # The mascott of the species (= what every guy have to look like)
        self.mascott = player
        self.fitnessSum = 0
        self.champ = player
        self.maximumFitness = 0
        # Count how many generations the species didn't evolved in a row
        self.stuck = 0

# -------------------------------------------------------------------------------------------------------- 

    def addPlayer(self, player):
        ''' Add a player to the species '''
        self.people.append(player)
        
# -------------------------------------------------------------------------------------------------------- 

    def sameSpecies(self, player):
        ''' Check if a genome belong to the species '''
        # Get the number of disjoint genes, ecess genes and the weight diefference with the mascott
        disjoint, excess, weight = self.countGenes(player)
        # Number of genes
        nbGenes = max(len(self.mascott.brain.connections), len(player.brain.connections))
        nbGenes = max(nbGenes-20, 1)
        # Compute the genomic distance
        distance = self.coefDisjoint/nbGenes * disjoint + self.coefExcess/nbGenes * excess + self.coefWeight * weight
#        print('Distance : ', distance)
        # If the distance is below the treshold, they belong to the same species !
        if distance < self.distanceTreshold:
            return True
        else:
            return False
        
# -------------------------------------------------------------------------------------------------------- 

    def countGenes(self, player):
        ''' Count the number of disjoint, excess and the weight difference ''' 
        disjoint = 0
        excess = 0
        weightDifference = 0
        matching = 0
        if self.mascott.fitness > player.fitness:
            brain1 = self.mascott.brain
            brain2 = player.brain
        else:
            brain1 = player.brain
            brain2 = self.mascott.brain
            
        # What is the max innovation number of brain1 ? - used to say if a gene is disjoint or excess
        maxInnovation = 0
        for connection1 in brain1.connections:
            # Store the max Innovation number
            if connection1.innovationNumber > maxInnovation:
                maxInnovation = connection1.innovationNumber
            # Check if the gene if matching or disjoint
            found = False
            for connection2 in brain2.connections:
                if connection1.innovationNumber == connection2.innovationNumber:
                    # Matching gene
                    weightDifference += abs(connection1.weight - connection2.weight)
                    matching += 1
                    found = True
                    break
            if not found:
                # Disjoint
                disjoint += 1
                
        # Now check the excess genes
        for connection2 in brain2.connections:
            match = False
            for connection1 in brain1.connections:
                if connection1.innovationNumber == connection2.innovationNumber:
                    match = True
                    break # Matching
            if not match:
                if connection2.innovationNumber > maxInnovation:
                    excess += 1
                else:
                    disjoint += 1
            
        # Get the average of the weight difference :
        if weightDifference != 0:
            weightDifference = weightDifference / matching
#        print('D : {}, E : {}, M : {}, W : {}'.format(disjoint, excess, matching, weightDifference))
        return disjoint, excess, weightDifference
            
# -------------------------------------------------------------------------------------------------------- 

    def newMascott(self):
        ''' Pick a new random mascott in the species '''
        self.mascott = np.random.choice(self.people)            

# -------------------------------------------------------------------------------------------------------- 

    def shareFitness(self):
        ''' Simple stuff '''
        for player in self.people:
            player.fitness = player.fitness / len(self.people)
            # Update the maximum fitness
            if player.fitness > self.maximumFitness:
                self.champ = player
#                # Reset the stuck counter !
#                self.stuck = 0
        self.stuck += 1
        self.updateFitnessSum()
        if self.fitnessSum / len(self.people) > self.maximumFitness:
            self.stuck = 0
                

# -------------------------------------------------------------------------------------------------------- 

    def updateFitnessSum(self):
        ''' Simple stuff '''
        self.fitnessSum = 0
        for player in self.people:
            self.fitnessSum += player.fitness

# -------------------------------------------------------------------------------------------------------- 

    def sort(self):
        ''' Sort the players : best first '''
        sortedList = [self.people[0]]
        for player in self.people[1:]:
            found = False
            for i in range(len(sortedList)):
                if player.fitness > sortedList[i].fitness:
                    sortedList.insert(i, player)
                    found = True
                    break
            if not found:
                sortedList.append(player)
        self.people = sortedList
                    
# -------------------------------------------------------------------------------------------------------- 

    def killBadPlayers(self):
        ''' Kill the bottom half of the species '''
        middle = int(len(self.people)/2)+1
        self.people = self.people[:middle]
            
# -------------------------------------------------------------------------------------------------------- 

    def clear(self):
        ''' Clear the species '''
        self.people = []
        
# -------------------------------------------------------------------------------------------------------- 

    def getBaby(self, innovationHistory):
        ''' Get a child within the species '''
        # In 25% cases, let the player pass with only a muation
        if np.random.rand() < 0.25:
            child = copy(self.selectPlayer())
        # In the other 75% we apply crossover then a mutation
        else:
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()
            # Be sure we use crossover with the fitest parent
            if parent2.fitness > parent1.fitness:
                parent1, parent2 = parent2, parent1
            child = copy(parent1)
            child.brain = parent1.brain.crossover(parent2.brain)     
        # Don't forget the mutation
        child.brain.mutate(innovationHistory)
        return child

# -------------------------------------------------------------------------------------------------------- 

    def selectPlayer(self):
        ''' Select a player based on it's fitness '''
        # Normalise the fitnesses
        scores = []
        for player in self.people:
            scores.append(player.fitness)
        scores = np.array(scores)
        proportions = list(scores / scores.sum())
        # Pick a random player
        return np.random.choice(self.people, p = proportions)
        
        
        
        
        
        
        
        
        
        
        
        
        
            