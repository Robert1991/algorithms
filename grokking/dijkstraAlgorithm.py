def findLowestCostNode(costs, processed):
    currentLowestNode = None
    currentLowestCost = float("inf")
    for node in costs:
        if costs[node] <= currentLowestCost and node not in processed:
            currentLowestNode = node
            currentLowestCost = costs[node]
    return currentLowestNode

graph = {}
graph["start"] = {}
graph["start"]["a"] = 5
graph["start"]["b"] = 2
graph["a"] = {}
graph["a"]["c"] = 4
graph["a"]["d"] = 2
graph["b"] = {}
graph["b"]["a"] = 8
graph["b"]["d"] = 7
graph["c"] = {}
graph["c"]["d"] = 6
graph["c"]["Fin"] = 3
graph["d"] = {}
graph["d"]["Fin"] = 1
graph["Fin"] = {}

parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["c"] = None
parents["d"] = None
parents["Fin"] = None

costs = {}
costs["a"] = 6
costs["b"] = 2
costs["c"] = float("inf")
costs["d"] = float("inf")
costs["Fin"] = float("inf")

processed = []
node = findLowestCostNode(costs, processed)

while node is not None:
    cost = costs[node]
    neighbors = graph[node]

    print(node)
    if node not in processed:
        for n in neighbors:
            new_costs = cost + neighbors[n]

            if costs[n] > new_costs:
                costs[n] = new_costs
                parents[n] = node
        processed.append(node)
        node = findLowestCostNode(costs, processed)

print(costs)
print(parents)