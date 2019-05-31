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