def quickSort(inputs):
    if (len(inputs) < 2):
        return inputs
    else:
        pivot = inputs[0]
        less = [i for i in inputs[1:] if i <= pivot]
        more = [i for i in inputs[1:] if i > pivot]
        return quickSort(less) + [pivot] + quickSort(more)

print(str(quickSort([5, 33, 2, 1, 24, 22])))