from random import random, randint
import randomTools

class GeneticAlgorithm:
    @staticmethod
    def runFor(allActions, population, inputBitString, currentPredictors, crate=0.8):
        return GeneticAlgorithm(allActions, population).runGaFor(inputBitString, currentPredictors, crate)
    
    def __init__(self, allActions, population):
        self.allActions = allActions
        self.formerPopulation = population

    def runGaFor(self, inputBitString, currentPredictors, crate):
        parent1, parent2 = self._binaryTournament_(currentPredictors), self._binaryTournament_(currentPredictors)
        child1, child2 = parent1.copy(), parent2.copy()
        child1, child2 = self._crossover_(parent1, parent2, child1, child2)
        self._mutateAndInsert_(child1, inputBitString), self._mutateAndInsert_(child2, inputBitString)
        return self.formerPopulation
        
    def _binaryTournament_(self, currentPredictors):
        while True:
            parent1Index = randint(0, len(currentPredictors)-1)
            parent2Index = randint(0, len(currentPredictors)-1)
            if parent1Index != parent2Index:
                break
        return (self.formerPopulation[parent1Index] if self.formerPopulation[parent1Index].fitness > self.formerPopulation[parent2Index].fitness 
                                                    else self.formerPopulation[parent2Index])
    
    def _crossover_(self, parent1, parent2, child1, child2):
        return self._crossoverChild_(child1, parent1, parent2), self._crossoverChild_(child2, parent1, parent2)
    
    def _mutateAndInsert_(self, child, randomBitString, mutationRate=0.04):
        mutated = self._mutateChild_(child, mutationRate, randomBitString)
        self._insertInPopulation_(mutated)

    def _insertInPopulation_(self, mutated):
        for classifier in self.formerPopulation:
            if classifier.condition == mutated.condition and classifier.action == mutated.action:
                classifier.number += 1
                return
        self.formerPopulation.append(classifier)

    def _crossoverChild_(self, child, parent1, parent2):
        child.condition = self._uniformCrossoverOfCondition_(parent1.condition, parent2.condition)
        child.prediction = (parent1.prediction+parent2.prediction) / 2
        child.error = 0.25 * (parent1.error+parent2.error) / 2
        child.fitness = 0.1 * (parent1.fitness+parent2.fitness) / 2
        return child    
    
    def _uniformCrossoverOfCondition_(self, parent1Condition, parent2Condition):
        crossoverCondition = ""
        for conditionIndex in range(len(parent1Condition)):
            crossoverCondition += parent1Condition[conditionIndex] if random() > 0.5 else parent2Condition[conditionIndex]
        return crossoverCondition
    
    def _mutateChild_(self, child, mutationRate, randomBitString):
        newChildCondition = ""
        for conditionIndex in range(len(child.condition)):
            if random() < mutationRate:
                newChildCondition += str(randomBitString[conditionIndex] if child.condition[conditionIndex] == "#" else "#")
            else:
                newChildCondition += child.condition[conditionIndex]
        child.condition = newChildCondition

        if random() < mutationRate:
            subset = [action for action in self.allActions if action != child.action]
            child.action = subset[0] if len(subset) == 1 else subset[randint(0, len(subset)-1)]
        return child

class Classifier:
    class RandomClassifierFactory:
        def __init__(self, inputBitString, actions):
            self.inputBitString = inputBitString
            self.actions = actions

        def create(self, currentGeneration, rate=1.0/3.0):
            return Classifier(self._createRandomInputCondition_(self.inputBitString, rate), self._randomActionFrom_(self.actions), currentGeneration)

        def _randomActionFrom_(self, actions):
            if len(actions) == 1:
                return actions[0]
            return actions[randint(0, len(actions)-1)]

        def _createRandomInputCondition_(self, inputBitString, rate):
            condition = ""
            for i in range(len(inputBitString)):
                if random() < rate:
                    condition += '#' 
                else:
                    condition += str(inputBitString[i])
            return condition
        
    fitness = 10.0
    prediction = 10.0
    error = 0.0
    expierence = 0.0
    setSize = 1.0
    number = 1.0
    action = None
    condition = None
    lastTimeCalled = -1
    deletionVote = 0.0

    @staticmethod
    def random(inputBitString, actions, currentGeneration, rate=1/3):
        return Classifier.RandomClassifierFactory(inputBitString, actions).create(currentGeneration, rate)

    def __init__(self, condition, action, birthGeneration):
        self.action = action
        self.condition = condition
        self.lastTimeCalled = birthGeneration
    
    def copy(self):
        copied = Classifier(self.condition, self.action, self.lastTimeCalled)
        copied.fitness = self.fitness
        copied.prediction = self.prediction
        copied.error = self.error
        copied.setSize = self.setSize
        copied.deletionVote = self.deletionVote
        copied.number = 1.0
        copied.expierence = 0.0
        return copied

    def predict(self):
        return self.prediction * self.fitness, self.fitness
    
    def doesMatch(self, inputBitString):
        for index, inputBit in enumerate(inputBitString):
            if self.condition[index] != "#":
                if inputBit != int(self.condition[index]): 
                    return False
        return True
    
    def calculateDeletionVote(self, avgFitness, deletionThreshHold, fThreshHold = 0.1):
        if self.expierence > deletionThreshHold and self.deratedFitness() < fThreshHold * avgFitness:
            self.deletionVote = self.vote() * (avgFitness / self.deratedFitness())
        else:
            self.deletionVote = self.vote()
        return self.deletionVote

    def vote(self):
        return self.setSize * self.number

    def deratedFitness(self):
        return self.fitness / self.number

    def updateSet(self, numberOfEquallyPredictedClassifiers, reward, beta):
        self.expierence += 1

        if self.expierence < 1.0/beta:
            self.error = (self.error * (self.expierence - 1) + abs(reward - self.prediction)) / self.expierence
            self.prediction = (self.prediction * (self.expierence - 1) + reward) / self.expierence
            self.setSize = (self.setSize * (self.expierence - 1) + numberOfEquallyPredictedClassifiers) / self.expierence
        else:
            self.error += beta * (abs(reward - self.prediction) - self.error)
            self.prediction += beta * (reward - self.prediction)
            self.setSize += beta * (numberOfEquallyPredictedClassifiers - self.setSize)

    def coversAnyActionIn(self, allActions):
        return self.action in allActions

class ClassifierSystem:
    def __init__(self, allActions, populationSize):
        self.allActions = allActions
        self.maxPopulationSize = populationSize
        self.population = []
        self.currentGeneration = 0
    
    def train(self, maximumGenerations, targetFunction, geneticAlgorithmFrequency=25):
        self.population = []
        performedPredictions = []
        for generation in range(maximumGenerations):
            randomInput = randomTools.randomBitString(6)
            randomInputMatchSet = self._createMatchSetFrom_(randomInput)
            predictedAction, prediction = self._predictActionFor_(randomInputMatchSet)
            reward = 1000 if targetFunction(randomInput) == predictedAction else 0

            if self._isExploringGeneration_():
                currentPredictors = [classifier for classifier in randomInputMatchSet if classifier.action == predictedAction]
                self._updateClassifiers_(currentPredictors, reward)
                
                if self._canRunGeneticAlgorithm_(currentPredictors, geneticAlgorithmFrequency):
                    for classifier in currentPredictors:
                        classifier.lastTimeCalled = self.currentGeneration
                    self.population = GeneticAlgorithm.runFor(self.allActions, self.population, randomInput, currentPredictors)
                    while len(self.population) > self.maxPopulationSize:
                        self._reducePopulationIfNecassary_()
            else:
                performedPredictions.append({'error' : abs(prediction[predictedAction]["weight"] - reward), 'wasCorrect' : True if reward == 1000 else False})

                if len(performedPredictions) >= 50:
                    error = sum(prediction["error"] for prediction in performedPredictions)/len(performedPredictions)
                    accuracy = sum(1 if prediction["wasCorrect"] else 0 for prediction in performedPredictions)/len(performedPredictions)
                    print("Generation " + str(self.currentGeneration) + " performs at a accuarcy " + str(accuracy) + " with error " + str(error))
                    performedPredictions = []

            self.currentGeneration += 1

    def predictActionFor(self, inputBitString):
        prediction = self._createPredictionFor_(self._createMatchSetFrom_(inputBitString))
        weightedActions = {}
        for key, value in prediction.items():
            weightedActions[key] = value["weight"]
        return sorted(weightedActions.items(), key = lambda keyValue: keyValue[1], reverse=True)[0][0]
    
    def _canRunGeneticAlgorithm_(self, currentPredictors, geneticAlgorithmFrequency):
        if len(currentPredictors) > 2:
            total = sum(classifier.lastTimeCalled * classifier.number for classifier in self.population)
            sumOfAllPredictors = sum(classifier.number for classifier in self.population)
            return True if self.currentGeneration - (total/sumOfAllPredictors) > geneticAlgorithmFrequency else False
        return False

    def _predictActionFor_(self, matchSet, explore = False):
        prediction = self._createPredictionFor_(matchSet)
        if explore:
            return prediction.keys()[randint(0, len(prediction)-1)]
        else:
            weightedActions = {}
            for key, value in prediction.items():
                weightedActions[key] = value["weight"]
            return sorted(weightedActions.items(), key = lambda keyValue: keyValue[1], reverse=True)[0][0], prediction

    def _createPredictionFor_(self, matchSet):
        prediction = {}
        for classifier in matchSet:
            key = classifier.action
            if key not in prediction:
                prediction[key] = {"predSum" : 0.0, "count" : 0.0, "weight" : 0.0}
            predSum, predFitness = classifier.predict()
            prediction[key]["predSum"] += predSum
            prediction[key]["count"] += predFitness
        for predictionKey, items in prediction.items():
            if items["count"] > 0:
                prediction[predictionKey]["weight"] = prediction[predictionKey]["predSum"]/prediction[predictionKey]["count"]
        return prediction
        
    def _createMatchSetFrom_(self, inputBitString):
        matchingClassifiers = [ citizen for citizen in self.population if citizen.doesMatch(inputBitString) ]
        coveredActions = set([ classifier.action for classifier in matchingClassifiers if classifier.coversAnyActionIn(self.allActions)])
        
        if len(coveredActions) < len(self.allActions):
            while True:
                remainingActions = [action for action in self.allActions if action not in coveredActions]
                newClassifier = Classifier.random(inputBitString, remainingActions, self.currentGeneration)
                matchingClassifiers.append(newClassifier)
                self.population.append(newClassifier)
                coveredActions.add(newClassifier.action)
                self._reducePopulationIfNecassary_()
                if len(coveredActions) >= len(self.allActions):
                    break
        return matchingClassifiers

    def _updateClassifiers_(self, correctClassifiers, reward, beta=0.2):
        updatedClassifiers = self._updateClassifierSet_(correctClassifiers, beta, reward)
        return self._updateClassifierFitness_(updatedClassifiers)
        
    def _updateClassifierSet_(self, correctClassifiers, beta, reward):
        numberOfCorrectClassifieres = 0
        for classifier in correctClassifiers:
            numberOfCorrectClassifieres += classifier.number
        for classifier in correctClassifiers:
            classifier.updateSet(numberOfCorrectClassifieres, reward, beta)
        return correctClassifiers
    
    def _updateClassifierFitness_(self, correctClassifiers, minimumError = 10, learningRate = 0.2, alpha = 0.1, v=-5.0):
        fitnessSum = 0
        classifierAccuracy = []

        for classifier in correctClassifiers:
            classifierAccuracy.append(1.0 if classifier.error < minimumError else alpha * (classifier.error/minimumError)**v)
            fitnessSum += classifierAccuracy[-1] * classifier.number
        for index, classifier in enumerate(correctClassifiers):
            classifier.fitness += learningRate * ((classifierAccuracy[index] * classifier.number) / fitnessSum - classifier.fitness)


    def _reducePopulationIfNecassary_(self, deletionThreshHold = 20.0):
        if sum(classifier.number for classifier in self.population) > self.maxPopulationSize:
            totalClassifiers = sum(classifier.number for classifier in self.population)
            averageFitness = sum(classifier.fitness/totalClassifiers for classifier in self.population)
            deletionVoteSum = sum(classifier.calculateDeletionVote(averageFitness, deletionThreshHold) for classifier in self.population)
            randomPointInDeletionVoteSum = random() * deletionVoteSum

            currentDeletionVoteSum = 0
            deletionIndex = -1
            for index, classifier in enumerate(self.population):
                currentDeletionVoteSum += classifier.deletionVote
                if currentDeletionVoteSum >= randomPointInDeletionVoteSum:
                    deletionIndex = index

            if self.population[deletionIndex].number > 1:
                self.population[deletionIndex].number -= 1
            else:
                self.population.pop(index)

    def _isExploringGeneration_(self):
        return self.currentGeneration % 2 == 0

def negate(bit):
    return 0 if bit == 1 else 1

def targetFunction(bitString):
    return negate(bitString[0])*negate(bitString[1])*bitString[0] + negate(bitString[0])*bitString[1]*bitString[3] + bitString[0]*negate(bitString[1])*bitString[4] * bitString[0]*bitString[1]*bitString[5]

classifierSystem = ClassifierSystem([0,1], 150)
classifierSystem.train(10000, targetFunction)

maxTrails = 100
correct = 0
for i in range( maxTrails):
    randInput = randomTools.randomBitString(6)
    predicted = classifierSystem.predictActionFor(randInput)
    if predicted == targetFunction(randInput):
        correct += 1
        
print("Accuracy: " + str(correct/maxTrails))
