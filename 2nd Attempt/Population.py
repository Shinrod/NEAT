# -*- coding: utf-8 -*-
from Player import Player
from Species import Species
import numpy as np
from copy import copy

# --------------------------------------------------------------------------------------------------------
class Population:
    
# --------------------------------------------------------------------------------------------------------

    def __init__(self, demography):
        ''' Make a population '''
        self.demography = demography
        # Keep track of the innovations that occured
        self.innovationHistory = []
        self.people = []
        # Fill the population
        for i in range(self.demography):
            player = Player()
#            player.brain.mutate(self.innovationHistory)
            self.people.append(player)
        # Store species
        self.species = []
        self.gen = 0
        self.best = self.people[0]
        
        # Store the best of each generation
        self.bests = []
        # Store the average fitness of all the species of each generation
        self.average = []
       
# --------------------------------------------------------------------------------------------------------

    def updateAlive(self):
        ''' Update all the players that are alive '''
        for player in self.people:
            if player.alive:
                player.update()

# --------------------------------------------------------------------------------------------------------

    def updateBest(self):
        ''' Simple stuff '''
        for s in self.species:
            if self.best is None or s.champ.fitness > self.best.fitness:
                self.best = copy(s.champ)
        self.bests.append(copy(self.best))
                
# --------------------------------------------------------------------------------------------------------

    def naturalSelection(self):
        ''' Make a new generation based on the old one '''
        self.prepare()
        # Kill the bottom half of each species so that only the best can reproduce
        self.killBadPlayers()
        # Kille the species that have not improved in 15 generations
        self.killStuckSpecies()
        
        # Proceed to repopulation !
        newPeople = []
        # If a species has 5 or more nets in it, the best pass without mutation
        for s in self.species:
            if len(s.people) >= 5:
                newPeople.append(s.champ)
            
        for i in range(self.demography - len(newPeople)):
            # In 0.1 % cases, 2 nets that are not in the same species can mate
            if np.random.rand() < 0.001:
                parent1 = self.selectSpecies().selectPlayer()
                parent2 = self.selectSpecies().selectPlayer()
                # Be sure we use crossover with the fitest parent
                if parent2.fitness > parent1.fitness:
                    parent1, parent2 = parent2, parent1
                child = copy(parent1)
                child.brain = parent1.brain.crossover(parent2.brain)
                # Don't forget the mutation
                child.brain.mutate(self.innovationHistory)
            # In 99.9% cases, the mating happen in the same species
            else:
                s = self.selectSpecies()
                child = s.getBaby(self.innovationHistory)
            newPeople.append(child)
        # Finish the new generation !
        self.people = newPeople
        self.gen += 1
        

# --------------------------------------------------------------------------------------------------------
    
    def evaluate(self):
        ''' Get the fitness of each player '''
        for player in self.people:
            player.evaluate()
            
# --------------------------------------------------------------------------------------------------------

    def newMascott(self):
        ''' Update the mascott for each species '''
        for s in self.species:
            s.newMascott()
            
# --------------------------------------------------------------------------------------------------------

    def fillSpecies(self):
        ''' Fill the species with the population '''
        # Clear the species
        for s in self.species:
            s.clear()
        # We fill them back
        for player in self.people:
            foundSpecies = False
            for s in self.species:
                if s.sameSpecies(player):
                    s.addPlayer(player)
                    foundSpecies = True
                    break
            # If we haven't found a species, make a new one
            if not foundSpecies:
                s = Species(player)
                self.species.append(s)

# --------------------------------------------------------------------------------------------------------

    def killEmptySpecies(self):
        ''' Simple stuff '''
        for i in list(range(len(self.species)))[::-1]:
            if len(self.species[i].people) == 0:
                self.species.pop(i)

# --------------------------------------------------------------------------------------------------------

    def killBadPlayers(self):
        ''' Kill the bottom half of each species '''
        for s in self.species:
            s.killBadPlayers()

# --------------------------------------------------------------------------------------------------------

    def killStuckSpecies(self):
        ''' Kill the species that have not improved in 15 generations '''
        for i in list(range(len(self.species)))[::-1]:
            if self.species[i].stuck >= 15:
                self.species.pop(i)
                
# --------------------------------------------------------------------------------------------------------

    def selectSpecies(self):
        ''' Pick a random species based on the sum of the fitnessSums '''
        # Normalise the fitnessSums
        scores = []
        for s in self.species:
            scores.append(s.fitnessSum)
        scores = np.array(scores)
        proportions = list(scores / scores.sum())
        # Pick a random species
        return np.random.choice(self.species, p = proportions)   
            
# --------------------------------------------------------------------------------------------------------

    def shareFitness(self):
        ''' Share the fitness within a species '''
        for s in self.species:
            s.shareFitness()
        
# --------------------------------------------------------------------------------------------------------

    def sortPlayers(self):
        ''' Sort the players in all the species '''
        for s in self.species:
            s.sort()

# --------------------------------------------------------------------------------------------------------

    def calcAverageFitness(self):
        ''' Get the average fitness of the species '''
        average = 0
        for s in self.species:
            average += s.fitnessSum / len(s.people)
        average = average / len(self.species)
        self.average.append(average)
           
# --------------------------------------------------------------------------------------------------------

    def prepare(self):
        ''' Prepare the generation for natural selection '''
        # Get the fitness
        self.evaluate()
        # Get a new mascott for each species
        try:
            self.newMascott()
        except:
            print(self.species)
            raise 'Error'
        # Fill the species with the population
        self.fillSpecies()
        # Kill the empty species
#        print('Species before killing empty ones : ', len(self.species))
        self.killEmptySpecies()
#        print('Species before killing empty ones', len(self.species))
        # Share the fitness within a species
        self.shareFitness()
        # Sort the best players in each species
        self.sortPlayers()
        # Update the best player
        self.updateBest()
        # Store the average fitness
        self.calcAverageFitness()
        















