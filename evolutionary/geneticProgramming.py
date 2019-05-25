import random

class Terminal:
    terminalValue = None

    @staticmethod
    def fromTerms(terms, valueBounds):
        term = terms[random.randint(0, len(terms)-1)]
        return Terminal(random.uniform(valueBounds[0], valueBounds[1]) if term == "R" else term)
    
    def __init__(self, terminalValue):
        self.terminalValue = terminalValue

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

    def hasInputArgs(self):
        return self.arg1 and self.arg2

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
            
    def fitness(self, targetFunction, trails=20):
        cumulatedError = 0.0
        for trail in range(trails):
            inputVal = random.uniform(-1, 1)
            result = self._evalProgramm(inputVal)
            print(result)
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
            
            if arg2 == 0 and program.function.operator == ":":
                return 0
            else:
                #print("inputVal: " + str(inputValue))
                print("op: " + str(program.function.operator) + " " + str(arg1) + " " +  str(arg2))
                #print("result: " + str(self._calculateFunctionValue(program.function.operator, arg1, arg2)))
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

        

        
def targetFunction(input):
    return input ** 2 + input + 1


functions = ["+","-","*","/"]
terms = ["X", "R"]

maxGenerations = 100
maxDepth = 3
populationSize = 100
bounds = 5
pReproduction = 0.08
pCrossover = 0.9
pMutation = 0.02

programms = []
program = Program.random(maxDepth, functions, terms, [-5,5])
print(program.printOut())
print(program.fitness(targetFunction, 1))
#for count in range(1):
    #programms.append()
    #print(programms[0].fitness(targetFunction, 20))
    #print(programms[0].printOut())
    
