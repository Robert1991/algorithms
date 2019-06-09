import math
import random

def randomGaussian(mean=0.0, stdDev=1.0):
    lower, upper, w = 0.0, 0.0, 0.0

    while True:
        lower = 2 * random.uniform(0,1) - 1
        upper = 2 * random.uniform(0,1) - 1
        w = lower * lower + upper * upper
        if w < 1:
            break
    w = math.sqrt((-2 * math.log(w)) / w)
    return mean + upper * w * stdDev

def randomVectorIn(bounds):
    randomVector = []
    for vectorBound in bounds:
        randomVector.append(vectorBound[0] + ((vectorBound[1] - vectorBound[0]) * random.random()))
    return randomVector

def randomIn(bounds):
    return random.uniform(bounds[0], bounds[1])

def randomBitString(numberOfBits):
    return [1 if random.random() > 0.5 else 0 for num in range(numberOfBits)]