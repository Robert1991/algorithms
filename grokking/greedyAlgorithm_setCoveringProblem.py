states_needed = set(["mt", "wa", "or", "id", "nv", "ut", "ca", "az"])

stations = {}
stations["kone"] = set(["id", "nv", "ut"])
stations["ktwo"] = set(["wa", "id", "mt"])
stations["kthree"] = set(["or", "nv", "ca"])
stations["kfour"] = set(["nv", "ut"])
stations["kfive"] = set(["ca", "az"])

finalStations = set()

while states_needed:
    bestStation = None
    statesCovered = set()

    for station, statesForStation in stations.items():
        covered = states_needed & statesForStation

        if len(covered) > len(statesCovered):
            bestStation = station
            statesCovered = covered

    states_needed -= statesCovered
    finalStations.add(bestStation)
    print(states_needed)

print(finalStations)