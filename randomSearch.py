import random
import math as math

def createRandomVector(searchSpace):
        randomVector = []
        for dimension in searchSpace:
                randomVector.append(random.uniform(dimension[0], dimension[1]))
        return randomVector

def targetFunction(inputs):
        cost = 0

        for inputValue in inputs:
                cost += math.pow(inputValue, 2) + inputValue + 24
        return cost


maxIterations = 10000

problemXMin = -5
problemXMax = 5
problemSize = 5
searchSpace = [[problemXMin,problemXMax] for i in range(problemSize)]

print("Minimizing: sum of x^2 + x + 24 in " + str(searchSpace))
bestSolution = []
lowestCost = float("inf")
for iteration in range(maxIterations):
        candidate = createRandomVector(searchSpace)
        candidateCost = targetFunction(candidate)
        if candidateCost < lowestCost:
                bestSolution = candidate
                lowestCost = candidateCost
                print(str(candidate) + " is now the best candidate with a cost of" + str(candidateCost))

print(str(bestSolution) + " won with a cost of " + str(lowestCost))
