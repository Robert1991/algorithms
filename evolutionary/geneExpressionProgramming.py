import random
import randomTools

class Node:
    def __init__(self, genomeChar):
        self.genomeChar = genomeChar
        self.leftNode = None
        self.rightNode = None
    
    def leftNeighbor(self, leftNode):
        self.leftNode = Node(leftNode)

    def rightNeighbor(self, rightNode):
        self.rightNode = Node(rightNode)

    def nextNodeToTheLeft(self):
        return self.leftNode

    def nextNodeToTheRight(self):
        return self.rightNode
    
    def expression(self):
        return self.genomeChar

class Genome:
    @staticmethod
    def random(grammer, headLength, tailLength):
        genome = []
        for gene in range(headLength):
            selection = grammer["FUNC"] if random.random() < 0.5 else grammer["TERM"]
            genome.append(selection[random.randint(0, len(selection) - 1)])

        [genome.append(grammer["TERM"][random.randint(0, len(grammer["TERM"]) - 1)]) for gene in range(tailLength)]
        return Genome(genome, grammer)
    
    def __init__(self, genome, grammer):
        self.genome = genome
        self.grammer = grammer

    def genomeIdentity(self):
        return self.genome

    def fitness(self, objectiveFunction, bounds, numTrails=30):
        meanError = 0.0

        for trail in range(numTrails):
            try:
                trailInputValue = randomTools.randomIn(bounds)
                meanError += abs(objectiveFunction(trailInputValue) - self._executeFunctionWith_(trailInputValue))
            except ZeroDivisionError:
                return float("inf")
        return meanError / numTrails

    def toString(self):
        return self._functionTreeToString_(self._mapGenomeToFunctionTree_())

    def _executeFunctionWith_(self, inputValue):
        function = self._functionTreeToString_(self._mapGenomeToFunctionTree_())
        return eval(function.replace("x", str(inputValue)))

    def _functionTreeToString_(self, tree):
        if not tree.nextNodeToTheLeft() or not tree.nextNodeToTheRight():
            return tree.expression()
        else:
            left = self._functionTreeToString_(tree.nextNodeToTheLeft())
            right = self._functionTreeToString_(tree.nextNodeToTheRight())

            return "(" + left + " " + tree.expression() + right + ")"

    def _mapGenomeToFunctionTree_(self):
        genomeOffset, queue = 0, []
        rootNode = Node(self.genome[genomeOffset])
        queue.append(rootNode)
        genomeOffset += 1

        while queue:
            currentNode = queue.pop(0)
            if currentNode.expression() in self.grammer["FUNC"]:
                currentNode.leftNeighbor(self.genome[genomeOffset])
                queue.append(currentNode.nextNodeToTheLeft())
                genomeOffset += 1
                currentNode.rightNeighbor(self.genome[genomeOffset])
                genomeOffset += 1
                queue.append(currentNode.nextNodeToTheRight())
        return rootNode
    
    def __eq__(self, other):
        if isinstance(other, Genome):
            return self.genome == other.genome
        return False

class Population:
    @staticmethod
    def randomPopulation(populationSize, grammer, genomeHeadLength, genomeTailLength):
        return Population([Genome.random(grammer, headLength, tailLength) for randomCitizen in range(populationSize)])
    
    def __init__(self, citizens):
        self.citizens = citizens
        self.n = len(citizens)

    def citizenAt(self, index):
        return self.citizens[index]

    def bestPerformingCitizen(self, objectiveFunction, bounds):
        self.citizens.sort(key=lambda citizen: citizen.fitness(objectiveFunction, bounds))
        return self.citizens[0]

    def parentsFromBinaryTournament(self, objectiveFunction, bounds):
        parentsForNextGen = []
        for parentIndex in range(len(self.citizens)):
            parent1, parent2 = self._randomParentsForTournament_()
            parentsForNextGen.append(parent1 if parent1.fitness(objectiveFunction, bounds) < parent2.fitness(objectiveFunction, bounds) else parent2)
        return Population(parentsForNextGen)
    
    def mergeWith(self, childGeneration, objectiveFunction, bounds):
        newPopulation = self.citizens + childGeneration.citizens
        newPopulation.sort(key=lambda citizen: citizen.fitness(objectiveFunction, bounds))
        return Population(newPopulation[0:self.n-1])

    def _randomParentsForTournament_(self):
        parent1 = self._randomCitizen_()

        while True:
            parent2 = self._randomCitizen_()
            if parent1 != parent2:
                break
        return parent1, parent2
    
    def _randomCitizen_(self):
        return self.citizens[random.randint(0, len(self.citizens)-1)]


class GeneExpressionProgramming:
    @staticmethod
    def initialize(populationSize, grammer, headLength, tailLength):
        return GeneExpressionProgramming(Population.randomPopulation(populationSize, grammer, headLength, tailLength), grammer, headLength, tailLength)
    
    def __init__(self, population, grammer, headLength, tailLength):
        self.population = population
        self.grammer = grammer
        self.headLength = headLength
        self.tailLength = tailLength
    
    def findFunctionFor(self, objectiveFunction, bounds, pCrossover=0.85, maxGenerations=50):
        currentBest = self.population.bestPerformingCitizen(objectiveFunction, bounds)
        for generation in range(maxGenerations):
            selectedForReproduction = self.population.parentsFromBinaryTournament(objectiveFunction, bounds)
            childGeneration = self._reproducePopulation_(selectedForReproduction, pCrossover)
            bestChild = childGeneration.bestPerformingCitizen(objectiveFunction, bounds)

            if bestChild.fitness(objectiveFunction, bounds) < currentBest.fitness(objectiveFunction, bounds):
                currentBest = bestChild
                print("Found new best function in generation " + str(generation) + " with fitness " + str(currentBest.fitness(objectiveFunction, bounds)) + " and function " + currentBest.toString())
            self.population = self.population.mergeWith(childGeneration, objectiveFunction, bounds)
        
    
    def _reproducePopulation_(self, selectedForReproduction, pCrossover):
        children = []
        for parent1Index, parent1 in enumerate(selectedForReproduction.citizens):
            if parent1Index == selectedForReproduction.n - 1:
                parent2 = selectedForReproduction.citizenAt(0)
            else:
                parent2 = selectedForReproduction.citizenAt(parent1Index + 1) if parent1Index % 2 == 0 else selectedForReproduction.citizenAt(parent1Index - 1) 

            child = self._crossoverParents_(parent1, parent2, pCrossover)
            child = self.pointMutate(child)
            children.append(child)
        return Population(children)

    def _crossoverParents_(self, parent1, parent2, pCrossover):
        if random.random() > pCrossover:
            return parent1
        else:
            childGenome = ""
            for parent1geneIndex, parent1Gene in enumerate(parent1.genomeIdentity()):
                childGenome += str(parent1Gene if random.random() < 0.5 else parent2.genomeIdentity()[parent1geneIndex])
            return Genome(childGenome, grammer)
    
    def pointMutate(self, child):
        childGenome = child.genomeIdentity()
        mutationRate = 1.0/len(childGenome)
        mutated = ""
        for i in range(len(childGenome)):
            bit = childGenome[i]

            if random.random() < mutationRate:
                if i < self.headLength:
                    selectedMutation = self.grammer["FUNC"] if random.random() < 0.5 else self.grammer["TERM"]
                    bit = selectedMutation[random.randint(0, len(selectedMutation) - 1)]
                else:
                    bit = self.grammer["TERM"][random.randint(0, len(grammer["TERM"]) - 1)]
            mutated += bit
        return Genome(mutated, grammer)

def objectiveFunction(input):
    return input**4 + input**3 + input**2 + input


grammer = {"FUNC" : ["+","-","*","/"], "TERM" : ["x"]}
bounds = [1,10]

headLength = 20
# 2 comes from the nodes of an operation, such as x * x -> 2
tailLength = headLength * (2 - 1) + 1

geneExpProgramming = GeneExpressionProgramming(Population.randomPopulation(80, grammer, headLength, tailLength),
            grammer, headLength, tailLength)
geneExpProgramming.findFunctionFor(objectiveFunction, bounds)