import randomTools
import math
import random

class Solution:
    @staticmethod
    def initRandom(bounds):
        strategy = [[0, (bounds[i][1]-bounds[i][0] * 0.05)] for i in range(len(bounds))]
        return Solution(randomTools.randomVectorIn(bounds), randomTools.randomVectorIn(strategy))

    def __init__(self, solution, strategy):
        self.solution = solution
        self.strategy = strategy
        self.winCount = 0

    def fitness(self, objectiveFunction):
        return objectiveFunction(self.solution)
    
    def wins(self):
        return self.winCount

    def tournamentWith(self, population, arenaSize, objectiveFunction):
        self.winCount = 0
        for fight in range(arenaSize):
            opponent = population[random.randint(0, populationSize - 1)]
            self.winCount += 1 if self.fitness(objectiveFunction) < opponent.fitness(objectiveFunction) else 0

    def mutate(self, searchSpace):
        childSolution = []
        childStrategy = []
        for index, solution in enumerate(self.solution):
            currentStrategy = self.strategy[index]
            newSolutionIndexValue = solution + currentStrategy * randomTools.randomGaussian()
            newSolutionIndexValue = searchSpace[index][0] if newSolutionIndexValue < searchSpace[index][0] else newSolutionIndexValue
            newSolutionIndexValue = searchSpace[index][1] if newSolutionIndexValue > searchSpace[index][1] else newSolutionIndexValue
            childSolution.append(newSolutionIndexValue)
            childStrategy.append(currentStrategy + randomTools.randomGaussian() * abs(currentStrategy)**0.5)
        return Solution(childSolution, childStrategy)

    def __eq__(self, other):
        return self.solution == other.solution and self.strategy == other.strategy

class Population:
    @staticmethod
    def createInitial(populationSize, bounds):
        return Population([Solution.initRandom(bounds) for i in range(populationSize)], bounds)

    def __init__(self, population, searchSpace):
        self.population = population
        self.searchSpace = searchSpace

    def best(self, objectiveFunction):
        self.population.sort(key=lambda citizen: citizen.fitness(objectiveFunction))
        return self.population[0]

    def unionWith(self, childPopulation, arenaSize, objectiveFunction):
        union = []
        for solution in self.population:
            if solution not in childPopulation.population:
                union.append(solution)
        [union.append(childSolution) for childSolution in childPopulation.population]
        [union[i].tournamentWith(union, arenaSize, objectiveFunction) for i in range(len(union))]
        union.sort(key=lambda candidate: candidate.wins(), reverse=True)
        return Population(union[0:len(self.population)], self.searchSpace)

    def reproduce(self):
        return Population([solution.mutate(self.searchSpace) for solution in self.population], searchSpace)

def objectiveFunction(solutionVector):
    solutionSum = 0
    for solution in solutionVector:
        solutionSum += solution**2
    return solutionSum

problemSize = 2
searchSpace = [[-5,5] for i in range(problemSize)]
maxGenerations = 1000
populationSize = 100
arenaSize = 5

population = Population.createInitial(populationSize, searchSpace)
currentBest = population.best(objectiveFunction)

for generation in range(maxGenerations):
    childPopulation = population.reproduce()

    if currentBest.fitness(objectiveFunction) > childPopulation.best(objectiveFunction).fitness(objectiveFunction):
        currentBest = childPopulation.best(objectiveFunction)
    population = population.unionWith(childPopulation, arenaSize, objectiveFunction)
    print("Generation " + str(generation) + "; current fitness: " + str(currentBest.fitness(objectiveFunction)) + "; solution: " + str(currentBest.solution))
    