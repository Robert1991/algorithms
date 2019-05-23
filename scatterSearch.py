import math
import random

class ObjectiveFunction:
    def cost(self, xValues):
        costs = 0
        for xValue in xValues:
            costs += math.pow(xValue, 2)
        return costs

class ValueBoundary:
    upper = float("inf")
    lower = float("inf")
    interval = [upper, lower]

    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower
        self.interval = [lower, upper]

class ProblemBoundaries:
    n = 0
    upper = 0
    lower = 0
    boundaries = []

    def __init__(self, problemSize, lower, upper):
        self.upper = upper
        self.lower = lower
        [self.boundaries.append(ValueBoundary(upper, lower)) for i in range(problemSize)]
        self.n = len(self.boundaries)
    
    def randomSolution(self):
        solutionVector = []

        for valueBound in self.boundaries:
            solutionVector += [random.uniform(valueBound.lower, valueBound.upper)]
        return solutionVector    
    
    def calcStepSizeWith(self, factor):
         return stepSizeFactor * (self.upper - self.lower)

class CountinousLocalSearch:
    maxNumberOfNoImprovements = 0
    problemBoundaries = None
    objectiveFunction = None

    def __init__(self, boundaries, maxNumberOfNoImprovements, objectiveFunction):
        self.problemBoundaries = boundaries
        self.maxNumberOfNoImprovements = maximumNumberOfNoImprovements
        self.objectiveFunction = objectiveFunction

    def performLocalSearchWithStepSizeBeginingWith(self, candidate, stepSize):
        noImprovementCount = 0
        currentBest = candidate
        
        while noImprovementCount < maximumNumberOfNoImprovements:
            newCanditate = self._createStepAwaySolution(currentBest, stepSize)

            if (self.objectiveFunction.cost(newCanditate) < self.objectiveFunction.cost(currentBest)):
                noImprovementCount = 0
                currentBest = newCanditate
                print("found better local solution: " + str(ObjectiveFunction().cost(currentBest)))
            else:
                noImprovementCount += 1
        return currentBest
    
    def _createStepAwaySolution(self, solution, stepSize):
        aStepAwaySolution = []

        for i in range(len(solution)):
            newLowerBound = max([self.problemBoundaries.boundaries[i].lower] + [solution[i] - stepSize])
            newUpperBound = min([self.problemBoundaries.boundaries[i].upper] + [solution[i] + stepSize])
            aStepAwaySolution.append(random.uniform(newLowerBound, newUpperBound))
        return aStepAwaySolution

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

class ReferenceSets:
    referenceSets = []

    def __init__(self, referenceSets):
        self.referenceSets = referenceSets

    def first(self):
        return self.referenceSets[0]
    
    def last(self):
        return self.referenceSets[-1]
    
    def exchangeLastReferenceSetWith(self, new):
        self.referenceSets.pop(-1)
        self.referenceSets.append(new)

    def all(self):
        return self.referenceSets

    def outdateAllReferenceSets(self):
        for referenceSet in self.referenceSets:
            referenceSet.newReferenceSet = False
    
    def sortAfterSolutionCost(self):
        self.referenceSets.sort(key=lambda ref: ref.solutionCost())

    def subsets(self):
        additions = [newReferenceSet for newReferenceSet in self.referenceSets if newReferenceSet.newReferenceSet]
        remainder = [remaining for remaining in self.referenceSets if remaining not in additions]
        remainder = additions if len(remainder) == 0 else remainder

        subsets = []
        for addition in additions:
            for remaining in remainder:
                if (addition != remaining and [addition, remaining] not in subsets):
                    subsets.append(SubSet([addition, remaining]))
        return subsets
    
    def __contains__(self, referenceSet):
        if (isinstance(referenceSet, ReferenceSet)):
            return referenceSet in self.referenceSets
        return False

    def __len__(self):
        return len(self.referenceSets)

class DiversSet:
    diversSet = []

    @staticmethod
    def initial(randomSolution, localSearch, stepSize):
        diverseSet = []

        while len(diverseSet) != diverseSetSize:
            candidate = localSearch.performLocalSearchWithStepSizeBeginingWith(randomSolution, 
                        stepSize)

            if (candidate not in diverseSet):
                diverseSet.append(candidate)
        return DiversSet(diverseSet)

    def __init__(self, diversSet):
        self.diversSet = diversSet
    
    def diversify(self, objectiveFunction, noElite, referenceSetSize):
        sortedDiverseSolutionSet = self._sortSolutionSetAfterCost(objectiveFunction)
        referenceSets = [ReferenceSet(sortedDiverseSolutionSet[elite]) for elite in range(noElite)]
        remainder = [notAlreadyInReferenceSet for notAlreadyInReferenceSet in sortedDiverseSolutionSet if notAlreadyInReferenceSet not in referenceSets]
        remainder.sort(key=lambda remaining : self._euclideanDistanceBetween(remaining, referenceSets))
        referenceSets = referenceSets + [ ReferenceSet(remaining) for remaining in remainder[:(referenceSetSize - len(referenceSets))]]
        return ReferenceSets(referenceSets)
    
    def _sortSolutionSetAfterCost(self, objectiveFunction):
        sortedDiverseSolutionSet = self.diversSet.copy()
        sortedDiverseSolutionSet.sort(key=lambda solution : objectiveFunction.cost(solution))
        return sortedDiverseSolutionSet

    def _euclideanDistanceBetween(self, remaining, referenceSets):
        distance = 0
        for referenceSet in referenceSets:
            for i in range(len(remaining)):
                distance += math.pow(remaining[i] - referenceSet.solution[i], 2)
        return math.sqrt(distance)


class SubSet:
    referenceSet1 = None
    referenceSet2 = None
    _subset = []

    def __init__(self, values):
        self.referenceSet1 = values[0]
        self.referenceSet2 = values[1]
        self._subset = values
    
    def recombine(self):
        centers = []
        for solutionIndex in range(len(self.referenceSet1.solution)):
            centers.append((self.referenceSet2.solution[solutionIndex] - self.referenceSet1.solution[solutionIndex]) / 2)
    
        childrenReferenceSets = []
        for solutionIndex in range(len(self._subset)):
            direction = 1 if random.random() < 0.5 else -1
            rand = random.random()
            child = []
            for bound in range(problemBoundaries.n):
                child.append(self._subset[solutionIndex].solution[bound] + direction * rand * centers[bound])        
                child[-1] = problemBoundaries.boundaries[bound].lower if child[-1] < problemBoundaries.boundaries[bound].lower else child[-1]
                child[-1] = problemBoundaries.boundaries[bound].upper if child[-1] > problemBoundaries.boundaries[bound].upper else child[-1]
            childrenReferenceSets.append(ReferenceSet(child))
        return childrenReferenceSets

class ScatterSearch:
    problemBoundaries = None
    localSearch = None

    def __init__(self, problemBoundaries, localSearch):
        self.problemBoundaries = problemBoundaries
        self.localSearch = localSearch
    
    def findBestSolution(self, maxIterations, stepSizeFactor, diversSetSize, referenceSetSize):
        inital = DiversSet.initial(problemBoundaries.randomSolution(), localSearch,problemBoundaries.calcStepSizeWith(stepSizeFactor))
        referenceSets = inital.diversify(ObjectiveFunction(), noElite, referenceSetSize)

        change = False
        for iteration in range(maximumIterations):
            subsets = referenceSets.subsets()
            referenceSets.outdateAllReferenceSets()
            change = self._exploreSubsetsForBetterReferenceSets(subsets, referenceSets)
            referenceSets.sortAfterSolutionCost()
            print("best reference set is now: " + str(referenceSets.first().solutionCost()))
            print("solution: " + str(referenceSets.first().solution))

            if (change == False):
                break

    def _exploreSubsetsForBetterReferenceSets(self, subsets, referenceSets):
        referenceSetChanged = False
        improved = []

        for subset in subsets:
            for recombined in subset.recombine():
                improved.append(localSearch.performLocalSearchWithStepSizeBeginingWith(recombined.solution, 
                            problemBoundaries.calcStepSizeWith(stepSizeFactor)))

        for betterSolution in improved:
            if ReferenceSet(betterSolution) not in referenceSets:
                newReferenceSet = ReferenceSet(betterSolution)
                referenceSets.sortAfterSolutionCost()

                if (newReferenceSet.solutionCost() < referenceSets.last().solutionCost()):
                    referenceSets.exchangeLastReferenceSetWith(newReferenceSet)
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

problemBoundaries = ProblemBoundaries(3, lowerBound, upperBound)
localSearch = CountinousLocalSearch(problemBoundaries, maximumNumberOfNoImprovements, ObjectiveFunction())

ScatterSearch(problemBoundaries, localSearch).findBestSolution(maximumIterations, stepSizeFactor, diverseSetSize, referenceSetSize)



