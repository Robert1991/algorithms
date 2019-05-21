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
                cost += math.pow(inputValue, 2)# + inputValue + 24
        return cost

def calculateLargeStepSize(currentIteration, searchDirectionFlipFactor, stepSize, largeFactor, smallFactor):
    if (currentIteration > 0):
        if (currentIteration % searchDirectionFlipFactor == 0):
            return stepSize * largeFactor
    return stepSize * smallFactor

def takeStep(searchSpace, currentPosition, stepSize):
    newPosition = []

    for position in range(len(currentPosition)):
        lower = max([searchSpace[position][0], currentPosition[position]-stepSize])
        upper = min([searchSpace[position][1], currentPosition[position]+stepSize])
        newPosition.append(random.uniform(lower, upper))
    return newPosition

problemXMin = -5
problemXMax = 5
problemSize = 2
searchSpace = [[problemXMin,problemXMax] for i in range(problemSize)]

maxIterations = 1000
initialStepSizeFactor = 0.05
stepSizeSmallFactor = 1.3
stepSizeLargeFactor = 3.0
searchDirectionFlipFactor = 10
maximumStepsWithoutImprovement = 30


stepSize = (searchSpace[0][1] - searchSpace[0][0])

currentBest = createRandomVector(searchSpace)
currentBestCost = targetFunction(currentBest)
currentCount = 0

for iteraton in range(maxIterations):
    largeStepSize = calculateLargeStepSize(iteraton, searchDirectionFlipFactor, stepSize, stepSizeLargeFactor, stepSizeSmallFactor)
    currentBigStep = takeStep(searchSpace, currentBest, largeStepSize)
    currentSmallStep = takeStep(searchSpace, currentBest, stepSize)
    
    if targetFunction(currentSmallStep) <= currentBestCost or targetFunction(currentBigStep) <= currentBestCost:
        if targetFunction(currentBigStep) <= currentBestCost:
            stepSize = largeStepSize
            currentBest = currentBigStep
            currentBestCost = targetFunction(currentBigStep)
        else:
            currentBest = currentSmallStep
            currentBestCost = targetFunction(currentSmallStep)
        currentCount = 0
    else:
        currentCount += 1

        if (currentCount >= maximumStepsWithoutImprovement):
            stepSize = 0
        else:
            stepSize = stepSize/stepSizeSmallFactor
    print(str(iteraton) + " best: " + str(currentBest) + " at cost " + str(currentBestCost))
    
    