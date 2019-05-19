from collections import deque

def personIsAvocadoSeller(personName):
    return personName[-1] == 'y'

graph = {}

graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["anuj"] = []
graph["claire"] = ["thom", "johnny"]
graph["peggy"] = []
graph["thom"] = []
graph["johnny"] = []

search_queue = deque()
search_queue += graph["you"]

alreadyProcessed = []

while search_queue:
    person = search_queue.popleft()

    if person not in alreadyProcessed:
        if personIsAvocadoSeller(person):
            print('This person sells avocados: ' + person)
            break
        else:
            search_queue += graph[person]
            alreadyProcessed.append(person)