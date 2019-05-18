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


#countDown(10)
print(fact(5))