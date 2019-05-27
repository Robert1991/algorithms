from Program import Program
from geneticProgramming import Population
from geneticProgramming import runGeneticProgramming
import sys

import random

def targetFunction(input):
    return input ** 2 + input + 1

functions = ["+","-","*","/"]
terms = ["X", "R"]

maxGenerations = 1000
maxDepth = 7
populationSize = 100
tournamentSelectionSize = 5
pReproduction = 0.08
pCrossover = 0.87
pMutation = 0.05

runGeneticProgramming(targetFunction, maxGenerations, populationSize, functions, terms)