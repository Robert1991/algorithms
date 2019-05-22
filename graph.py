import matplotlib.pyplot as plt
import sys, math, random, heapq
from itertools import chain

class Tour:
    def __init__(self, g, vertices = None):
        """Generate random tour in given graph g"""
        self.g = g

        if vertices is None:
            self.vertices = list(range(1, g.n))
            random.shuffle(self.vertices)
        else:
            self.vertices = vertices
        self.__cost = None

    def cost(self):
        """Return total edge-cost of tour"""
        if self.__cost is None:
            self.__cost = 0
            for i, j in zip([0] + self.vertices, self.vertices + [0]):
                self.__cost += self.g.distance(self.g.vertices[i], self.g.vertices[j])
        return self.__cost
    
    def utilities(self, penalties):
        
        utilities = []
        for i, j in zip([0] + self.vertices, self.vertices + [0]):
            utilities.append(self.g.distance(self.g.vertices[i], self.g.vertices[j]) / (1 + penalties[i][j])) 

        return utilities
    
    def augmentedCost(self, _lambda, penalties):
        augmentedCost = 0
        for i, j in zip([0] + self.vertices, self.vertices + [0]):
            currentDistance = self.g.distance(self.g.vertices[i], self.g.vertices[j])
            augmentedCost += currentDistance + _lambda * penalties[i][j]
        return augmentedCost

    def stochasticTwoOpt(self):
        c1 = random.randint(0, len(self.vertices))
        exclude = [c1]
        exclude.append(len(self.vertices) - 1) if c1 == 0 else exclude.append(c1-1)
        exclude.append(0) if c1 == len(self.vertices)-1 else exclude.append(c1+1)

        c2 = random.randint(0, len(self.vertices))
        while c2 in range(min(exclude), max(exclude)):
            c2 = random.randint(0, len(self.vertices))

        if (c2 < c1):
            c2Value = c2
            c2 = c1
            c1 = c2Value
        alteredSequence = self.vertices[c1:c2]
        alteredSequence.reverse()
        return Tour(self.g,  self.vertices[:c1] + alteredSequence + self.vertices[c2:])
    
    def performDoubleBridgeMove(self):
        pos1 = 1 + random.randint(0, len(self.vertices)/4)
        pos2 = pos1 + 1 + random.randint(0, len(self.vertices)/4)
        pos3 = pos2 + 1 + random.randint(0, len(self.vertices)/4)
        return Tour(self.g, self.vertices[0:pos1] + self.vertices[pos3:] 
                          + self.vertices[pos2:pos3] + self.vertices[pos1:pos2])




class Graph:
    distanceLookupCache = {}

    def __init__(self, vertices):
        self.vertices = vertices
        self.n = len(vertices)
     
    def x(self, v):
        return self.vertices[v][0]

    def y(self, v):
        return self.vertices[v][1]
     
    def calcEuclidean(self, verticle1, verticle2):
        return math.sqrt((verticle1[0] - verticle2[0])**2 + (verticle1[1] - verticle2[1])**2)

    def updateCache(self, verticle1, verticle2, distance):
        self.distanceLookupCache[(verticle1, verticle2)] = distance 
        self.distanceLookupCache[(verticle2, verticle1)] = distance
        return distance

    def distance(self, verticle1, verticle2):
        if (verticle1, verticle2) in self.distanceLookupCache:
            return self.distanceLookupCache[(verticle1, verticle2)]
          
        return self.updateCache(verticle1, verticle2, self.calcEuclidean(verticle1, verticle2))

    def randomTour(self):
        return Tour(self)

    def plot(self, tour=None):
        """Plots the cities and superimposes given tour"""

        if tour is None:
            tour = Tour(self, [])
        _vertices = [self.vertices[0]]

        for i in tour.vertices:
            _vertices.append(self.vertices[i])
        _vertices.append(self.vertices[0])

        plt.title("Cost = " + str(tour.cost()))

        for verticle in self.vertices:
             plt.scatter(verticle[0], verticle[1], c="b", s=10, marker="s")
        for verticle in _vertices:
             plt.scatter(verticle[0], verticle[1], c="r")
        plt.show()