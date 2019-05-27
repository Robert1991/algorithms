import random
import sys

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
    _fitness = None
    function = None

    @staticmethod
    def random(maxDepth, functions, terms, valueBounds, depth=0, program=None):
        if depth == maxDepth - 1 or (depth > 1 and random.random() < 0.1):
            return Program(Terminal.fromTerms(terms, valueBounds))
        depth += 1

        return Program(Function(functions[random.randint(0, len(functions)-1)], Program.random(maxDepth, functions, terms, valueBounds, depth, program), Program.random(maxDepth, functions, terms, valueBounds, depth, program)))

    @staticmethod
    def prune(program, maxDepth, terms, currentDepth=0):
        if currentDepth == maxDepth -1:
            return Program(Terminal.fromTerms(terms, [-5,5]))
        else:
            currentDepth += 1
            if isinstance(program.function, Terminal):
                return program
            else:
                prunedArg1Prog = Program.prune(program.function.arg1, maxDepth, terms, currentDepth)
                prunedArg2Prog = Program.prune(program.function.arg2, maxDepth, terms, currentDepth)
                return Program(Function(program.function.operator, prunedArg1Prog, prunedArg2Prog))

    def __init__(self, function):
        self.function = function

    def copy(self):
        return Program(self.function.copy())

    def replaceAt(self, nodeIndex, replacement, lastProgram=None, currentIndex=0):
        lastProgram = self if not lastProgram else lastProgram
        if nodeIndex == currentIndex:
            currentIndex += 1
            return Program(replacement.function), currentIndex
        else:
            currentIndex += 1
            if isinstance(lastProgram.function, Terminal):
                return lastProgram, currentIndex
            else:
                arg1Node, currentIndex = self.replaceAt(nodeIndex, replacement, lastProgram=lastProgram.function.arg1, currentIndex=currentIndex)
                arg2Node, currentIndex = self.replaceAt(nodeIndex, replacement, lastProgram=lastProgram.function.arg2, currentIndex=currentIndex)

                return lastProgram, currentIndex
            

    def subProgramAt(self, nodeIndex, lastProgram=None, currentIndex=0):
        lastProgram = self if not lastProgram else lastProgram
        
        if nodeIndex == currentIndex:
            return lastProgram.copy(), currentIndex
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
            inputVal = random.uniform(-5, 5)
            result = self._evalProgramm(inputVal)
            cumulatedError += abs(result - targetFunction(inputVal))
        self._fitness = cumulatedError / trails
        return self._fitness

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
