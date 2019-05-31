from randomTools import randomGaussian
import random
import math

class Strategy:
    @staticmethod
    def createStrategiesFrom(valueBounds):
        strategies = []
        for valueBound in valueBounds:
            strategies.append(Strategy(valueBound))
        return strategies
    
    @staticmethod
    def mutateVector(strategies):
        tau = math.sqrt(2.0* len(strategies))**(-1)
        tau_p = math.sqrt(2.0* math.sqrt(len(strategies)))**(-1)

        childStrategies = []
        for index, strategy in enumerate(strategies):
            childStrategies.append(
                Strategy(strategy.bounds, strategy.standardDev() * math.exp(tau_p * randomGaussian() + tau*randomGaussian())))
        return childStrategies

    def __init__(self, bounds, strategy = None):
        self.bounds = bounds
        if not strategy:
            self.strategy = Solution.randomIn([[0, (bounds[1]- bounds[0]) * 0.05]])[0]
        else:
            self.strategy = strategy

    def standardDev(self):
        return self.strategy

    def __str__(self):
        return str(self.strategy)
    
    def __eq__(self, obj):
        return isinstance(obj, Strategy) and obj.strategy == self.strategy

class Solution:
    @staticmethod
    def randomIn(bounds):
        return [bounds[i][0] + (bounds[i][1] - bounds[i][0]) * random.random() for i in range(len(bounds))]
    
    @staticmethod
    def createInitial(bounds):
        return Solution(Solution.randomIn(bounds), Strategy.createStrategiesFrom(bounds), bounds)
    
    def __init__(self, solutionVector, strategy, searchSpace):
        self.solutionVector = solutionVector
        self.strategy = strategy
        self.searchSpace = searchSpace

    def fitness(self, objectiveFunction):
        return objectiveFunction(self.solutionVector)

    def mutateSolution(self):
        childSolutionVector = self._mutateSolutionVector_()
        return Solution(childSolutionVector, Strategy.mutateVector(self.strategy), self.searchSpace)
        

    def _mutateSolutionVector_(self):
        childSolutionVector = []
        for index, solution in enumerate(self.solutionVector):
            childSolutionVector.append(solution + self.strategy[index].standardDev() * randomGaussian())
            childSolutionVector[index] = self.searchSpace[index][0] if childSolutionVector[index] < self.searchSpace[index][0] else childSolutionVector[index]
            childSolutionVector[index] = self.searchSpace[index][1] if childSolutionVector[index] > self.searchSpace[index][1] else childSolutionVector[index]
        return childSolutionVector

    def __eq__(self, obj):
        return isinstance(obj, Solution) and obj.solutionVector == self.solutionVector and obj.strategy == self.strategy

    def __str__(self):
        return str(self.solutionVector) + "; " + str(self.strategy)

class Population:
    solutions = []

    @staticmethod
    def init(searchSpace, populationSize):
        pop = Population(populationSize)
        for i in range(populationSize):
            pop.add(Solution.createInitial(searchSpace))
        return pop
    
    def __init__(self, populationSize, solutions = []):
        self.populationSize = populationSize
        self.solutions = solutions
    
    def add(self, solution):
        self.solutions.append(solution)

    def reproduce(self, childCount):
        children = []
        for childIndex in range(childCount):
            children.append(self.solutions[childIndex].mutateSolution())
        return children

    def best(self, objectiveFunction):
        self.solutions.sort(key=lambda solution: solution.fitness(objectiveFunction))
        return self.solutions[0]
    
    def unionWith(self, children, objectiveFunction):
        unified = []
        for selfSolution in self.solutions:
            if selfSolution not in children:
                unified.append(selfSolution)
        [unified.append(child) for child in children]
        unified.sort(key=lambda solution: solution.fitness(objectiveFunction))
        return Population(self.populationSize, unified[0:self.populationSize]) 

def objectiveFunction(solutionVector):
    solutionSum = 0
    for solution in solutionVector:
        solutionSum += solution**2
    return solutionSum


maxGenerations = 100
childCount = 30

population = Population.init([[-5,5],[-5,5],[-5,5]], 40)
best = population.best(objectiveFunction)

for generation in range(maxGenerations):
    children = population.reproduce(childCount)
    population = population.unionWith(children, objectiveFunction)
    if best.fitness(objectiveFunction) > population.best(objectiveFunction).fitness(objectiveFunction):
        best = population.best(objectiveFunction)
        print("found better solution with cost: " + str(best.fitness(objectiveFunction)) + " in " + str(generation))