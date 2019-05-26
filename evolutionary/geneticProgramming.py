import random

class Terminal:
    terminalValue = None

    @staticmethod
    def fromTerms(terms, valueBounds):
        term = terms[random.randint(0, len(terms)-1)]
        return Terminal(random.uniform(valueBounds[0], valueBounds[1]) if term == "R" else term)
    
    def __init__(self, terminalValue):
        self.terminalValue = terminalValue
    
    def copy(self):
        return Terminal(self.terminalValue)

    def isInputValueTerminal(self):
        return self.terminalValue == "X"
    
    def randValueInBounds(self):
        return self.terminalValue


class Function:
    operator = None
    arg1 = None
    arg2 = None

    def __init__(self, function, arg1, arg2):
        self.operator = function
        self.arg1 = arg1
        self.arg2 = arg2
    
    def copy(self):
        return Function(self.operator, self.arg1, self.arg2)

class Program:
    function = None

    @staticmethod
    def random(maxDepth, functions, terms, valueBounds, depth=0, program=None):
        if depth == maxDepth - 1 or (depth > 1 and random.random() < 0.1):
            return Program(Terminal.fromTerms(terms, valueBounds))
        depth += 1

        return Program(Function(functions[random.randint(0, len(functions)-1)], Program.random(maxDepth, functions, terms, valueBounds, depth, program), Program.random(maxDepth, functions, terms, valueBounds, depth, program)))


    def __init__(self, function):
        self.function = function

    def copy(self):
        return Program(self.function.copy())

    def subProgramAt(self, nodeIndex, lastProgram=None, currentIndex=0):
        lastProgram = self if not lastProgram else lastProgram
        if nodeIndex == currentIndex:
            return lastProgram, currentIndex
        else:
            currentIndex += 1
            if isinstance(lastProgram.function, Terminal):
                return None, currentIndex
            else:
                arg1Node, currentIndex = self.subProgramAt(nodeIndex, lastProgram=lastProgram.function.arg1, currentIndex=currentIndex)

                if arg1Node:
                    return arg1Node, currentIndex
                
                arg2Node, currentIndex = self.subProgramAt(nodeIndex, lastProgram=lastProgram.function.arg2, currentIndex=currentIndex)

                if arg2Node:
                    return arg2Node, currentIndex
                
                return None, currentIndex


    def nodeCount(self, node = None):
        node = self if not node else node

        if isinstance(node.function, Terminal):
            return 1
        else:
            nodeCountArg1 = self.nodeCount(node.function.arg1)
            nodeCountArg2 = self.nodeCount(node.function.arg2)
            return nodeCountArg1 + nodeCountArg2 + 1

    def fitness(self, targetFunction, trails=20):
        cumulatedError = 0.0
        for trail in range(trails):
            inputVal = random.uniform(-1, 1)
            result = self._evalProgramm(inputVal)
            cumulatedError += abs(result - targetFunction(inputVal))
        return cumulatedError / trails

    def printOut(self, program=None):
        if not program:
            program = self
        if isinstance(program.function, (Terminal)):
            return program.function.terminalValue
        return "(#" + program.function.operator + " #" + str(self.printOut(program.function.arg1)) + " #" + str(self.printOut(program.function.arg2)) + ")"
            
    def _evalProgramm(self, inputValue, program=None):
        if not program:
            program = self

        if isinstance(program.function, Terminal):
            return inputValue if program.function.isInputValueTerminal() else program.function.randValueInBounds()
        else:
            arg1 = self._evalProgramm(inputValue, program.function.arg1)
            arg2 = self._evalProgramm(inputValue, program.function.arg2)
            
            if arg2 == 0.0 and program.function.operator == "/":
                return 0
            else:
                return self._calculateFunctionValue(program.function.operator, arg1, arg2)
    
    def _calculateFunctionValue(self, operator, arg1, arg2):
        if operator == "+":
            return arg1 + arg2
        elif operator == "-":
            return arg1 - arg2
        elif operator == "*":
            return arg1 * arg2
        else:
            return arg1 / arg2

class Population:
    @staticmethod
    def createRandomWith(populationSize, targetFunction):
        return Population([Program.random(maxDepth, functions, terms, [-5,5]) for i in range(populationSize)], targetFunction)
    
    def __init__(self, population, targetFunction):
        self.population = population
        self.targetFunction = targetFunction
        self.populationSize = len(population)

    def parentFromTournamentSelection(self, tournamentSelectionSize):
        selectedForTournament = [self.population[random.randint(0, self.populationSize-1)] for i in range(tournamentSelectionSize)]
        self.sort(selectedForTournament)
        [print(program.fitness(self.targetFunction)) for program in selectedForTournament]
        return selectedForTournament[0]

    def sort(self, population=None):
        population = self.population if not population else population
        population.sort(key=lambda citizen: citizen.fitness(targetFunction))
    
    def best(self):
        self.sort()
        return self.population[0]

def crossover(parent1, parent2):
    randomNodeIndexParent1 = random.randint(0, parent1.nodeCount()-2)
    randomNodeIndexParent2 = random.randint(0, parent2.nodeCount()-2)



def targetFunction(input):
    return input ** 2 + input + 1


functions = ["+","-","*","/"]
terms = ["X", "R"]

maxGenerations = 100
maxDepth = 3
populationSize = 100
tournamentSelectionSize = 5
pReproduction = 0.08
pCrossover = 0.9
pMutation = 0.02

population = Population.createRandomWith(populationSize, targetFunction)
population.sort()

for count in range(1):
    children = []    
    
    while len(children) < populationSize:
        randomOperation = random.random()

        parent1 = population.parentFromTournamentSelection(tournamentSelectionSize)

        if randomOperation < pReproduction:
            child = parent1.copy()
        elif randomOperation < pReproduction + pCrossover:
            parent2 = population.parentFromTournamentSelection(tournamentSelectionSize)
            print(parent2.printOut())
            print(parent2.nodeCount())
            for i in range(parent2.nodeCount()):
                print(parent2.subProgramAt(i)[0].printOut())    
        break


    
    
