from graph import Graph
from graph import Tour

class CandidateEntry:
    iteration = -1
    tour = None
    #Is one because it was met once on creation of the object
    vistedTimes = 1

    @staticmethod
    def generateFromStocasticTwoOptOf(currentTour):
        return CandidateEntry(currentTour.stochasticTwoOpt())

    def __init__(self, tour):
        self.tour = tour
    
    def tourEquals(self, otherTour):
        return self.tour.vertices == otherTour.vertices
    
    def wasVistedAtIteration(self, iteration):
        self.vistedTimes += 1
        self.iteration = iteration
        return self
    
    def tourCost(self):
        return self.tour.cost()

    def lastIterationWhenMet(self):
        return self.iteration

    def tourVertices(self):
        return self.tour.vertices

class TabuList:
    @staticmethod
    def create():
        return TabuList([])
    
    def __init__(self, tabuList):
        self.tabuList = tabuList

    def isTabu(self, candidate, iteration, prohibitionPeriod):
        for tabuCandidate in self.tabuList:
            if (candidate.tourVertices()[0] in tabuCandidate.tourVertices() or candidate.tourVertices()[1] in tabuCandidate.tourVertices()):
                return candidate.lastIterationWhenMet() >= iteration - prohibitionPeriod
        return False
    
    def makeTabu(self, candidate, iteration):
        for alreadyTabu in self.tabuList:
            if alreadyTabu.tourEquals(candidate.tour):
                alreadyTabu.wasVistedAtIteration(iteration)
                return alreadyTabu
        self.tabuList.append(candidate)
        return self.tabuList[-1]

    def empty(self):
        return len(self.tabuList) == 0

def getCandidateEntryFrom(visitedList, tour):
    for entry in visitedList:
        if entry.tourEquals(tour):
            return entry
    return None

def sortNeighboorhood(candidates, tabuList, iteration, prohibitionPeriod):
    tabus = []
    admissables = []
    for candidate in candidates:
        if tabuList.isTabu(candidate, iteration, prohibitionPeriod):
            tabus.append(candidate)
        else:
            admissables.append(candidate)
        
    return tabus, admissables

berlin52 = Graph([(565.0, 575.0), (25.0, 185.0), (345.0, 750.0), (945.0, 685.0), 
     (845.0, 655.0), (880.0, 660.0), (25.0, 230.0), (525.0, 1000.0), 
     (580.0, 1175.0), (650.0, 1130.0), (1605.0, 620.0), (1220.0, 580.0), 
     (1465.0, 200.0), (1530.0, 5.0), (845.0, 680.0), (725.0, 370.0), 
     (145.0, 665.0), (415.0, 635.0), (510.0, 875.0), (560.0, 365.0), 
     (300.0, 465.0), (520.0, 585.0), (480.0, 415.0), (835.0, 625.0), 
     (975.0, 580.0), (1215.0, 245.0), (1320.0, 315.0), (1250.0, 400.0), 
     (660.0, 180.0), (410.0, 250.0), (420.0, 555.0), (575.0, 665.0), 
     (1150.0, 1160.0), (700.0, 580.0), (685.0, 595.0), (685.0, 610.0), 
     (770.0, 610.0), (795.0, 645.0), (720.0, 635.0), (760.0, 650.0), 
     (475.0, 960.0), (95.0, 260.0), (875.0, 920.0), (700.0, 500.0), 
     (555.0, 815.0), (830.0, 485.0), (1170.0, 65.0), (830.0, 610.0), 
     (605.0, 625.0), (595.0, 360.0), (1340.0, 725.0), (1740.0, 245.0)])

maxIterations = 3000
maximumCandidates = 50
increase = 1.3
decrease = 0.9

currentTour = berlin52.randomTour()
bestTour = currentTour
tabuList = TabuList.create()
prohibitionPeriod = 1
visitedList = []
averageSize = 1
lastChange = 0

for iteration in range(maxIterations):
    canidateEntry = getCandidateEntryFrom(visitedList, currentTour)
    if canidateEntry == None:
        visitedList.append(CandidateEntry(currentTour).wasVistedAtIteration(iteration))
    else:
        repetitionInterval = iteration - canidateEntry.lastIterationWhenMet()
        canidateEntry.wasVistedAtIteration(iteration)

        if repetitionInterval < 2*(berlin52.n-1):
            averageSize = 0.1 * (iteration - canidateEntry.lastIterationWhenMet()) + 0.9 * averageSize
            prohibitionPeriod = prohibitionPeriod * increase
            lastChange = iteration
    if iteration - lastChange > averageSize:
        prohibitionPeriod = max([prohibitionPeriod*decrease, 1])
        lastChange = iteration
    
    candidates = []
    for cand in range(maximumCandidates):
        candidates.append(CandidateEntry.generateFromStocasticTwoOptOf(currentTour))
    candidates.sort(key=lambda candidate: candidate.tourCost())
    tabus, admissables = sortNeighboorhood(candidates, tabuList, iteration, prohibitionPeriod)

    if len(admissables) < 2:
        prohibitionPeriod = berlin52.n - 2
        lastChange = iteration
    
    currentCandidate = tabus[0] if len(admissables) == 0 else admissables[0]

    if not len(tabus) == 0:
        firstTabu = tabus[0]

        if firstTabu.tourCost() < bestTour.cost() and firstTabu.tourCost() < currentCandidate.tourCost():
            currentCandidate = firstTabu
    tabuList.makeTabu(currentCandidate, iteration)
    if candidates[0].tourCost() < bestTour.cost():
        bestTour = candidates[0].tour
    currentTour = currentCandidate.tour
    print("At iteration " + str(iteration) + " and prohibation period=" + str(prohibitionPeriod) + " the best was " + str(bestTour.cost()))
    
