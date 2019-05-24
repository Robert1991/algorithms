import math

def promptIntegerInput(promptMessage):
    userInput = raw_input(promptMessage)
    try:
        return int(userInput)
    except: ValueError
    print("Not an integer input " + userInput)

def floor(input):
    return int(math.floor(input))

searchSpaceLower = promptIntegerInput("What is the lower bound of the search space? > ")
searchSpaceUpper = promptIntegerInput("What is the upper bound of the search space? > ") + 1
searchedNumber = promptIntegerInput("Which number are you looking for > ")

if searchedNumber < searchSpaceLower or searchedNumber > searchSpaceUpper:
    print('I have no chance of finding a number outside my search space')
    exit()
else:
    searchRange = range(searchSpaceLower, searchSpaceUpper)
    iteration = 0
    foundSearchedNumber = False
    while foundSearchedNumber == False:
        inspectedNumber = searchRange[floor(abs(searchRange[0] - searchRange[-1])/2)]
        print('inspected ' + str(inspectedNumber))
        if (searchedNumber == inspectedNumber):
            print("found: " + str(inspectedNumber))
            foundSearchedNumber = True
            break
        elif inspectedNumber >= searchedNumber:
            searchRange = range(searchRange[0], inspectedNumber + 1)
        elif len(searchRange) == 2:
            if (foundSearchedNumber == searchRange[0]):
                print("found: " + str(searchRange[0]))
            else:
                print("found: " + str(searchRange[-1]))
            foundSearchedNumber = True
        else:
            searchRange = range(inspectedNumber, searchRange[-1] + 1)
        print('Search for ' + str(searchedNumber) + ' in range from ' + str(searchRange[0]) + ' to ' + str(searchRange[len(searchRange) - 1]))
        print('Iteration: ' + str(iteration))
        iteration += 1

