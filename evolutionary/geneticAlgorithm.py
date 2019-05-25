import random

def oneMax(bitVector):
    cost = 0
    for bit in bitVector:
        cost += bit
    return cost

def createRandomBitArrayWith(numberOfBits):
    bitArray = []
    for bitNumber in range(numberOfBits):
        bitArray.append(0) if random.random() <= 0.5 else bitArray.append(1)
    return bitArray

def binaryTournament(population):
    firstPick = random.randint(0, len(population)-1)
    
    while True:
        secondPick = random.randint(0, len(population)-1)
        if (secondPick != firstPick):
            break
    return population[firstPick] if oneMax(population[firstPick]) > oneMax(population[secondPick]) else population[secondPick]

def mutate(child, pMutation):
    mutated = []
    for bit in child:
        if random.random() < pMutation:
            mutated.append(0 if bit == 1 else 1)
        else:
            mutated.append(bit)
        
    return mutated

def crossover(parent1, parent2, pCrossover):
    if random.random() >= pCrossover:
        return parent1
    matchingPoint = 1 + random.randint(0, len(parent1) -2)
    return parent1[:matchingPoint] + parent2[matchingPoint:len(parent1)]


def reproducePopulation(selected, populationSize, pCrossover, pMutation):
    children = []

    for index, parent1 in enumerate(selected):
        parent2 = selected[index+1] if index % 2 == 0 else selected[index-1]
        if i == len(selected) -1:
            parent2 = selected[0]

        child = crossover(parent1, parent2, pCrossover)
        child = mutate(child, pMutation)
        children.append(child)

        if len(children) >= populationSize:
            break
    return children

numberOfBits = 64

maxGens = 10000
populationSize = 100

crossOverProbalility = 0.98
mutationProbalility = 1.0/numberOfBits

population = [createRandomBitArrayWith(numberOfBits) for i in range(populationSize) ]
population.sort(key=lambda citizen: oneMax(citizen))
best = population[-1]

for i in range(maxGens):
    selectedForNextGeneration = [binaryTournament(population) for i in range(populationSize)]
    children = reproducePopulation(selectedForNextGeneration, populationSize, crossOverProbalility, mutationProbalility)
    children.sort(key=lambda child: oneMax(child))

    if oneMax(children[0]) >= oneMax(best):
        best = children[0]
        print("found new best with cost: " + str(oneMax(best)))

        if oneMax(best) == numberOfBits:
            break
    population = children