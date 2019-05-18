def findCurrentMinIndex(inputArray):
    currentMinIndex = 0
    currentMinValue = inputArray[0]

    for i in range(1, len(inputArray)):
        if inputArray[i] <= currentMinValue:
            currentMinIndex = i
            currentMinValue = inputArray[i]
    return currentMinIndex

def selectionSort(inputArray):
    sorted = []

    for i in range(len(inputArray)):
        sorted.append(inputArray.pop(findCurrentMinIndex(inputArray)))
    return sorted


print(selectionSort([5, 3, 6, 2, 10]))