def countDown(numbers):
    if (numbers == 0):
        print("Boom")
        return
    else:
        print(str(numbers) + '...')
        countDown(numbers-1)

def fact(input):
    if (input == 1):
        return 1
    else:
        return input * fact(input-1)

def sumRec(inputArray, currentTotal = 0):
    if (len(inputArray) == 0):
       return str(currentTotal)
    else:
        currentTotal += inputArray.pop(0)
        return sumRec(inputArray, currentTotal=currentTotal) 

def totalItemNumRec(inputArray, currentCount = 0):
    if (len(inputArray) == 0):
       return str(currentCount)
    else:
        currentCount += 1
        inputArray.pop(0)
        return totalItemNumRec(inputArray, currentCount=currentCount) 

def maxNumberInListRec(inputArray, currentMax = 0):
    if (len(inputArray) == 0):
       return str(currentMax)
    else:
        if (inputArray[0] >= currentMax):
            currentMax = inputArray[0]
        inputArray.pop(0)
        return maxNumberInListRec(inputArray, currentMax=currentMax) 

#countDown(10)
#print(fact(5))
print('sum ' + str(sumRec([1, 2, 3, 4])))
print('totals ' + str(totalItemNumRec([1, 2, 3, 4])))
print('max ' + str(maxNumberInListRec([1, 22, 3, 4])))
#print()