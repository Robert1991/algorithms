import random
import randomTools

class Program:
    @staticmethod
    def decode(grammer, bitString, codonBits, maxDepth):
        operations = []
        for offSet in range(int(len(bitString)/codonBits)):
            codon = bitString[offSet * codonBits:(offSet * codonBits) + codonBits]
            operations.append(Program._intValueOf_(codon))
        return Program(Program.createProgramFrom(operations, grammer, maxDepth), bitString)

    @staticmethod
    def createProgramFrom(operations, grammer, maxDepth):
        done = False
        offset = 0
        currentDepth = 0
        symbolicString = grammer["S"]
        #print("symbolic string: " + symbolicString)
        #print(operations)
        while True:
            done = True
            for key, value in grammer.items():
                if key in symbolicString:
                    done = False
                    moves = grammer["VAR"] if key == "EXP" and currentDepth >= maxDepth-1 else value
                    #print(moves)
                    integer = operations[offset] % len(moves)
                    #print("operation int: " + str(operations[offset]))
                    #print(str(integer) + ": " + str(moves[integer]))
                    offset = 0 if offset==len(operations)-1 else offset + 1
                    symbolicString = symbolicString.replace(key, moves[integer], 1)
                    #print("symbolic string: " + symbolicString)
                    #print()
            currentDepth +=1
            if done:
                break
        return symbolicString


    @staticmethod
    def _intValueOf_(bitString):
        result = 0
        for index in range(len(bitString)):
            result += 2**index if(bitString[index] == 1) else 0
        return result
    
    def __init__(self, symbolicString, bitString):
        self.identity = bitString
        self.symbolicString = symbolicString

    def fitness(self, bounds, objectiveFunction, numTrails=60):
        if self.symbolicString.strip() == "INPUT":
            return float("inf")
        else:
            sumError = 0.0
            try:
                for trail in range(numTrails):
                    randomInput = random.uniform(bounds[0], bounds[1])
                    sumError += abs(self._executeProgram_(randomInput) - objectiveFunction(randomInput))
            except ZeroDivisionError:
                return float("inf")
        return sumError / numTrails

    def _executeProgram_(self, inputValue):
        initializedProgram = self.symbolicString.replace("INPUT", str(inputValue))
        return eval(initializedProgram)
    
    def __eq__(self, otherProgram):
        if isinstance(otherProgram, Program):
            return self.identity == otherProgram.identity
        return False


class Population:
    @staticmethod
    def random(populationSize, grammer, numberOfBits, codonBits, maxDepth):
        return Population([Program.decode(grammer, randomTools.randomBitString(numberOfBits), codonBits, maxDepth) for i in range(populationSize)])
    
    def __init__(self, programs):
        self.programs = programs
        self.size = len(programs)
    
    def best(self, objectiveFunction, bounds):
        self.programs.sort(key=lambda prog: prog.fitness(bounds, objectiveFunction))
        return self.programs[0]
    
    def mergeWith(self, otherPopulation):
        merged = self.programs + otherPopulation.programs
        merged.sort(key=lambda prog: prog.fitness(bounds, objectiveFunction))
        return Population(merged[0:self.size])

    def randomCitizen(self):
        return self.programs[random.randint(0, self.size-1)]
        
class GrammaticalEvolution:
    class BitStringModifications:
        @staticmethod
        def pointMutation(bitString):
            pointMutationRate = 1.0/len(bitString)
            for bitIndex in range(len(bitString)):
                if random.random() < pointMutationRate:
                    bitString[bitIndex] = 0 if bitString[bitIndex] == 1 else 1
            return bitString

        @staticmethod
        def onePointCrossover(parentBitString1, parentBitString2, codonBits, pCrossover):
            if random.random() < pCrossover:
                # the random position needs to be at the border of a codon bit, so the resulting string is a valid bit string again
                geneticCuttingPoint = (random.randint(0, min([len(parentBitString1), len(parentBitString2)])/codonBits)) * codonBits
                return parentBitString1[:geneticCuttingPoint] + parentBitString2[geneticCuttingPoint:]
            return parentBitString1

        @staticmethod
        def codonDuplication(bitString, codonBits):
            duplicationRate = 1.0/codonBits
            if random.random() < duplicationRate:
                randomCodonPostion = random.randint(0, len(bitString)/codonBits)
                return bitString + bitString[randomCodonPostion*codonBits:randomCodonPostion*codonBits+codonBits]
            return bitString
        
        @staticmethod
        def codonDeletion(bitString, codonBits):
            deletionRate = 1.0/codonBits
            if random.random() < deletionRate:
                randomCodonOffset = random.randint(0, len(bitString)/codonBits)
                return bitString[0:randomCodonOffset] + bitString[randomCodonOffset+codonBits:]
            return bitString
        
        

    def __init__(self, grammer, objectiveFunction, bounds):
        self.grammer = grammer
        self.objectiveFunction = objectiveFunction
        self.bounds = bounds

    def searchBestFunction(self, codonBits, populationSize=100, pCrossover=0.3, maxDepth=7, generations=100):
        currentBest, population = self._initializePopulation_(populationSize, codonBits, maxDepth)
        for generation in range(generations):
            selected = self._selectParentsForNextGeneration_(population)
            childPopulation = self._reproduceGenartionFrom_(selected, pCrossover, codonBits, maxDepth)
            bestChild = childPopulation.best(self.objectiveFunction, self.bounds)
            if self._candidateFitness_(bestChild) < self._candidateFitness_(currentBest):
                currentBest = bestChild
                print("Found better solution in generation " + str(generation) + " with function " + str(bestChild.symbolicString) + " and fitness " + str(self._candidateFitness_(bestChild)))
            population = population.mergeWith(childPopulation)
            print("searching... in generation " + str(generation) + " (current best fitness=" + str(self._candidateFitness_(currentBest)) + ")")
        print("best function was " + currentBest.symbolicString + " with fitness: " + str(self._candidateFitness_(currentBest)))
    
    def _selectParentsForNextGeneration_(self, population):
        selected = []
        for binaryTournament in range(population.size):
            selected.append(self._selectParentForNextGenerationThroughBinaryTournament_(population))
        return selected
    
    def _reproduceGenartionFrom_(self, selectedParents, pCrossover, codonBits, maxDepth):
        children = []
        for parentIndex, parent1 in enumerate(selectedParents):
            parent2 = self._selectSecondParentFor_(parentIndex, selectedParents)
            child = GrammaticalEvolution.BitStringModifications.onePointCrossover(parent1.identity, parent2.identity, codonBits, pCrossover)
            child = GrammaticalEvolution.BitStringModifications.codonDeletion(child, codonBits)
            child = GrammaticalEvolution.BitStringModifications.codonDuplication(child, codonBits)
            child = GrammaticalEvolution.BitStringModifications.pointMutation(child)
            children.append(Program.decode(self.grammer, child, codonBits, maxDepth))
        return Population(children)
    
    def _selectParentForNextGenerationThroughBinaryTournament_(self, population):
        while True:
            firstCandidateParent, secondCandidateParent = population.randomCitizen(), population.randomCitizen()
            if firstCandidateParent != secondCandidateParent:
                break
        return firstCandidateParent if self._candidateFitness_(firstCandidateParent) < self._candidateFitness_(secondCandidateParent) else secondCandidateParent

    def _initializePopulation_(self, populationSize, codonBits, maxDepth):
        population = Population.random(populationSize, grammer, 10*codonBits, codonBits, maxDepth)
        return population.best(self.objectiveFunction, self.bounds), population
    
    def _candidateFitness_(self, candidate):
        return candidate.fitness(self.bounds, self.objectiveFunction) 

    def _selectSecondParentFor_(self, parentIndex, selectedParents):
        parent2 = selectedParents[parentIndex+1] if parentIndex % 2 == 0 else selectedParents[parentIndex-1]
        return selectedParents[0] if parentIndex == len(selectedParents) - 1 else parent2


def objectiveFunction(inputVal):
    return inputVal**4 + inputVal**3 + inputVal ** 2+ inputVal

grammer = {"S" : "EXP",
           "EXP": [" EXP BINARY EXP ", " (EXP BINARY EXP) ", "VAR"],
           "BINARY" : ["+", "-", "/", "*"],
           "VAR" : ["INPUT", "1.0"]}
populationSize = 100
bounds = [1,100]
maxDepth = 7
codonBits = 4
numberOfBits = 10 * codonBits
pCrossover = 0.3

GrammaticalEvolution(grammer, objectiveFunction, bounds).searchBestFunction(codonBits, populationSize=100, generations=300)
