from randomTools import randomGaussian, randomVectorIn
import random

class Population:
    bounds = []


    @staticmethod
    def createInitial(populationSize, bounds):
        return Population([randomVectorIn(bounds) for i in range(populationSize)], bounds)
    
    def __init__(self, population, bounds):
        self.population = population
        self.bounds = bounds
        self.populationSize = len(population)
    
    def recreateFrom(self, children, objectiveFunction):
        newGeneration = []
        for index in range(len(self.population)):
            newGeneration.append(self.population[index] if objectiveFunction(self.population[index]) < objectiveFunction(children[index]) else children[index]) 
        return Population(newGeneration, self.bounds)

    def createChildGeneration(self, weightingFactor, crossoverRate):
        children = []

        for index, rootParent in enumerate(self.population):
            matingPartners = self._selectParentsOf_(index)
            children.append(self._binaryRandomRecombination_(rootParent, matingPartners, weightingFactor, crossoverRate))
        return children

    def sortAfter(self, objectiveFunction):
        self.population.sort(key=lambda solution: objectiveFunction(solution))
        return self
    
    def best(self, objectiveFunction):
        self.population.sort(key=lambda solution: objectiveFunction(solution))
        return self.population[0]

    def _binaryRandomRecombination_(self, rootParent, matingPartners, weightingFactor, crossoverRate):
        child = []
        cut = random.randint(0, len(rootParent) - 1) + 1

        for index, solution in enumerate(rootParent):
            child.append(solution)

            if index == cut or random.random() < crossoverRate:
                altered = self.population[matingPartners[2]][index] + weightingFactor * (self.population[matingPartners[0]][index] - self.population[matingPartners[1]][index])
                altered = self.bounds[index][0] if altered < self.bounds[index][0] else altered
                altered = self.bounds[index][1] if altered > self.bounds[index][1] else altered
                child[index] = altered
        return child

    def _selectParentsOf_(self, currentChildIndex):
        parent1 = self._randomCitizen_()
        while parent1 == currentChildIndex:
            parent1 = self._randomCitizen_()
        parent2 = self._randomCitizen_()
        while parent2 == currentChildIndex or parent2 == parent1:
            parent2 = self._randomCitizen_()
        parent3 = self._randomCitizen_()
        while parent3 == currentChildIndex or parent3 == parent2 or parent3 == parent1:
            parent3 = self._randomCitizen_()
        return [parent1, parent2, parent3]

    def _randomCitizen_(self):
        return random.randint(0, len(self.population)-1)

def objectiveFunction(solutionVector):
    solutionSum = 0
    for solution in solutionVector:
        solutionSum += solution**2
    return solutionSum

maxGenerations = 200
problemSize = 3
bounds = [[-5,5] for i in range(problemSize)]
populationSize = 10 * problemSize
weightingFactor = 0.8
crossoverRate = 0.9

population = Population.createInitial(populationSize, bounds).sortAfter(objectiveFunction)
best = population.best(objectiveFunction)

for generation in range(maxGenerations):
    children = population.createChildGeneration(weightingFactor, crossoverRate)
    population = population.recreateFrom(children, objectiveFunction)
    
    if objectiveFunction(population.best(objectiveFunction)) < objectiveFunction(best):
        best = population.best(objectiveFunction) 
        print("current best solution: " + str(best) + " with cost " + str(objectiveFunction(best)) + " found in generation " + str(generation))