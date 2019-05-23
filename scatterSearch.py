import math
import random

class ObjectiveFunction:
    def cost(self, xValues):
        costs = 0
        for xValue in xValues:
            costs += math.pow(xValue, 2)
        return costs

class ReferenceSet:
    solution = []
    newReferenceSet = True

    def __init__(self, eliteDiversSolution):
        """Generate a reference set from an elite divers solution"""        
        self.solution = eliteDiversSolution
        self.newReferenceSet = True

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, (list,)):
            return set(self.solution) & set(other)
        elif isinstance(other, ReferenceSet):
            return set(self.solution) & set(other.solution)
        return False

    def solutionCost(self):
        return ObjectiveFunction().cost(self.solution)    

def takeStepAwayFrom(solution, stepSize, bounds):
    aStepAwaySolution = []

    for i in range(len(solution)):
        newLowerBound = max([bounds[i][0]] + [solution[i] - stepSize])
        newUpperBound = min([bounds[i][1]] + [solution[i] + stepSize])
        aStepAwaySolution.append(random.uniform(newLowerBound, newUpperBound))
    return aStepAwaySolution

def localSearchSolutionIn(candidate, bounds, stepSize, maxNumberOfNoImprovements):
    noImprovementCount = 0

    currentBest = candidate
    while noImprovementCount < maximumNumberOfNoImprovements:
        newCanditate = takeStepAwayFrom(currentBest, stepSize, bounds)

        if (ObjectiveFunction().cost(newCanditate) < ObjectiveFunction().cost(currentBest)):
            noImprovementCount = 0
            currentBest = newCanditate
            print("found better local solution: " + str(ObjectiveFunction().cost(currentBest)))
        else:
            noImprovementCount += 1
    return currentBest    

def stepSize(stepSizeFactor, lower, upper):
    return stepSizeFactor * (upper - lower)

def randomSolutionInBounds(bounds):
    solutionVector = []

    for valueRestriction in bounds:
        solutionVector += [random.uniform(valueRestriction[0], valueRestriction[1])]
    return solutionVector

def euclideanDistanceBetween(remaining, referenceSets):
    distance = 0
    for referenceSet in referenceSets:
        for i in range(len(remaining)):
            distance += math.pow(remaining[i] - referenceSet.solution[i], 2)
    return math.sqrt(distance)

def sortSolutionSetAfterCost(diverseSolutionSet):
    sortedDiverseSolutionSet = diverseSolutionSet
    sortedDiverseSolutionSet.sort(key=ObjectiveFunction().cost)
    return sortedDiverseSolutionSet

def diversify(diverseSolutionSet, noElite, referenceSetSize):
    sortedDiverseSolutionSet = sortSolutionSetAfterCost(diverseSolutionSet)
    referenceSet = [ReferenceSet(diverseSolutionSet[elite]) for elite in range(noElite)]
    remainder = [notAlreadyInReferenceSet for notAlreadyInReferenceSet in sortedDiverseSolutionSet if notAlreadyInReferenceSet not in referenceSet]
    remainder.sort(key=lambda remaining : euclideanDistanceBetween(remaining, referenceSet))
    referenceSet = referenceSet + [ ReferenceSet(remaining) for remaining in remainder[:(referenceSetSize - len(referenceSet))]]
    return referenceSet

def constructInitialDiverseSet(stepSizeFactor, diverseSetSize, maxNumberOfNoImprovements, bounds):
    diverseSet = []

    while len(diverseSet) != diverseSetSize:
        candidate = randomSolutionInBounds(bounds)
        candidate = localSearchSolutionIn(candidate, bounds, stepSize(stepSizeFactor, bounds[0][0], bounds[0][1]), maxNumberOfNoImprovements)
        
        if (candidate not in diverseSet):
            diverseSet.append(candidate)
    return diverseSet


def createBoundsFor(problemSize, lower, upper):
    return [[lower, upper] for x in range(problemSize)]
        
def selectSubsetsFrom(referenceSets):
    additions = [newReferenceSet for newReferenceSet in referenceSets if newReferenceSet.newReferenceSet]
    remainder = [remaining for remaining in referenceSets if remaining not in additions]
    remainder = additions if len(remainder) == 0 else remainder

    subsets = []
    for addition in additions:
        for remaining in remainder:
            if (addition != remaining and [addition, remaining] not in subsets):
                subsets.append([addition, remaining])
    return subsets

def recombineSubSet(subset, bounds):
    referenceSet1 = subset[0]
    referenceSet2 = subset[1]

    centers = []
    for solutionIndex in range(len(referenceSet1.solution)):
        centers.append((referenceSet2.solution[solutionIndex] - referenceSet1.solution[solutionIndex]) / 2)
    
    childrenReferenceSets = []
    for solutionIndex in range(len(subset)):
        direction = 1 if random.random() < 0.5 else -1
        rand = random.random()
        child = []
        for bound in range(len(bounds)):
            child.append(subset[solutionIndex].solution[bound] + direction * rand * centers[bound])        
            child[-1] = bounds[bound][0] if child[-1] < bounds[bound][0] else child[-1]
            child[-1] = bounds[bound][1] if child[-1] > bounds[bound][1] else child[-1]
        childrenReferenceSets.append(ReferenceSet(child))
    return childrenReferenceSets
    
def exploreSubsetsForBetterReferenceSets(subsets, bounds, stepSize, maxNumberOfNoImprovements):
    referenceSetChanged = False
    for subset in subsets:
        recombinedSubsets = recombineSubSet(subset, bounds)

    improved = []
    for recombined in recombinedSubsets:
        print(recombined.solution)
        improved.append(localSearchSolutionIn(recombined.solution, bounds, stepSize, maxNumberOfNoImprovements))

    for betterSolution in improved:
        if ReferenceSet(betterSolution) not in referenceSets:
            newReferenceSet = ReferenceSet(betterSolution)
            referenceSets.sort(key=lambda ref: ref.solutionCost())

            if (newReferenceSet.solutionCost() < referenceSets[-1].solutionCost()):
                referenceSets.append(newReferenceSet)
                print("Added " + str(newReferenceSet.solution))
                print("Cost " + str(newReferenceSet.solutionCost()))
                referenceSetChanged = True
    return referenceSetChanged


problemSize = 3
lowerBound = -5
upperBound = 5
maximumIterations = 100
maximumNumberOfNoImprovements = 30
referenceSetSize = 10
diverseSetSize = 20
noElite = 5

stepSizeFactor = 0.005
bounds = createBoundsFor(3, -5, 5)
inital = constructInitialDiverseSet(stepSizeFactor, diverseSetSize, maximumNumberOfNoImprovements, bounds)
referenceSets = diversify(inital, noElite, referenceSetSize)
bestCurrentReferenceSet = referenceSets[0]

for iteration in range(maximumIterations):
    subsets = selectSubsetsFrom(referenceSets)

    for referenceSet in referenceSets:
        referenceSet.newReferenceSet = False

    change = exploreSubsetsForBetterReferenceSets(subsets, bounds, stepSize(stepSizeFactor, lowerBound, upperBound), maximumNumberOfNoImprovements)
    referenceSets.sort(key=lambda ref: ref.solutionCost())
    print("best reference set is now: " + str(referenceSets[0].solutionCost()))

    if change == False:
        break




