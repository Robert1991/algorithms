import random

def oneMax(bitVector):
    cost = 0
    for bit in bitVector:
        cost += bit
    return cost

def randomNeighbor(currentBitArray):
    mutant = currentBitArray
    randomPosition = random.randint(0, len(currentBitArray)-1)
    mutant[randomPosition] = 1 if mutant[randomPosition] == 0 else 0
    return mutant

def createRandomBitArrayWith(numberOfBits):
    bitArray = []
    for bitNumber in range(numberOfBits):
        bitArray.append(0) if random.random() <= 0.5 else bitArray.append(1)
    return bitArray

maxIterations = 90000000
bitArray = createRandomBitArrayWith(64)
currentBitArrayCost = oneMax(bitArray)

print(bitArray)
print(oneMax(bitArray))


for i in range(maxIterations):
    neighbor = randomNeighbor(bitArray)
    neighborCost = oneMax(neighbor)

    if neighborCost >= currentBitArrayCost:
        bitArray = neighbor
        currentBitArrayCost = neighborCost
        print(str(i) + " " + str(bitArray) + " with cost " + str(currentBitArrayCost))
    if currentBitArrayCost == len(bitArray):
        break