import random
from Program import Program

class Population:
    @staticmethod
    def crossover(parent1, parent2, maxDepth, terms):
        child1 = parent1.copy()
        child2 = parent2.copy()
        randomNodeIndexParent1 = random.randint(0, parent1.nodeCount()-2) + 1
        randomNodeIndexParent2 = random.randint(0, parent2.nodeCount()-2) + 1
        randomNodeParent1 = parent1.subProgramAt(randomNodeIndexParent1)[0]
        randomNodeParent2 = parent2.subProgramAt(randomNodeIndexParent2)[0]
        child2.replaceAt(randomNodeIndexParent2, randomNodeParent1)
        child1.replaceAt(randomNodeIndexParent1, randomNodeParent2)
        return Program.prune(child1, 4, terms), Program.prune(child2, 4, terms)

    @staticmethod
    def mutate(parent, maxDepth, functions, terms):
        randomProgram = Program.random(int(maxDepth/2), functions, terms, [-5,5])
        randomNodeIndex = random.randint(0, randomProgram.nodeCount()-1)
        child = parent.copy()
        child.replaceAt(randomNodeIndex, randomProgram.subProgramAt(randomNodeIndex)[0])
        return Program.prune(parent, maxDepth, terms)
        
    @staticmethod
    def createRandomWith(populationSize, targetFunction, maxDepth, functions, terms, bounds=[-5,5]):
        return Population([Program.random(maxDepth, functions, terms, bounds) for i in range(populationSize)], targetFunction)
    
    def __init__(self, population, targetFunction):
        self.population = population
        self.targetFunction = targetFunction
        self.populationSize = len(population)

    def parentFromTournamentSelection(self, tournamentSelectionSize):
        selectedForTournament = [self.population[random.randint(0, self.populationSize-1)] for i in range(tournamentSelectionSize)]
        self.sort(selectedForTournament)
        return selectedForTournament[0]

    def sort(self, population=None):
        population = self.population if not population else population
        population.sort(key=lambda citizen: citizen.fitness(self.targetFunction, 100))
    
    def best(self):
        return self.population[0]

def runGeneticProgramming(targetFunction, maxGenerations, populationSize, functions, terms, tournamentSelectionSize=5, maxDepth = 7, pReproduction=0.08, pCrossover = 0.87, pMutation = 0.05):
    population = Population.createRandomWith(populationSize, targetFunction, maxDepth, functions, terms)
    population.sort()
    currentBest = population.best()
    for count in range(maxGenerations):
        print(count)
        children = []    
    
        while len(children) < populationSize:
            randomOperation = random.random()

            parent1 = population.parentFromTournamentSelection(tournamentSelectionSize)
        
            if randomOperation < pReproduction:
                child1 = parent1.copy()
            elif randomOperation < pReproduction + pCrossover:
                parent2 = population.parentFromTournamentSelection(tournamentSelectionSize)
                child1, child2 = Population.crossover(parent1, parent2, maxDepth, terms)
                children.append(child2)
            else:
                child1 = Population.mutate(parent1, maxDepth, functions, terms)
        
            children.append(child1)

        population = Population(children, targetFunction)
        population.sort()

        if population.best().fitness(targetFunction, 100) < currentBest.fitness(targetFunction, 100):
            currentBest = population.best()
            print("found new best function with avg cost " + str(currentBest.fitness(targetFunction)) + " " + currentBest.printOut())

    print("found best function with avg cost " + str(currentBest.fitness(targetFunction, 100)) + " " + currentBest.printOut())
