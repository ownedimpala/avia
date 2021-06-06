import numpy as np

N = 4                                             # number of flights

DepartureAirport = ["VOZ", "LED", "SVO", "LED"]   # airports
ArrivalAirport = ["SVO", "ARH", "SVX", "MMK"]

DepartureTime = [6, 7, 8, 11]                     # times
ArrivalTime = [7, 8, 11, 13]

TransferDepartureAirport = ["SVO", "ARH"]         # transfer airports
TransferArrivalAirport = ["LED", "LED"]
TransferDuration = [1, 1]                         # transfer durations
TN = 2                                            # number of possible transfers

ServiceTime = 1                                   # service time in airports

AdjacencyMatrix = np.zeros(shape=(2 * N + 4, 2 * N + 4))      # adjacency matrix of the final graph

for i in range(N):                                # add flights to adjacency matrix
    AdjacencyMatrix[i + N, i] = 1

for i in range(N):                                # check if it is possible for a plane to wait or fly somewhere to perform the next flight
    for j in range(N):
        if ArrivalAirport[j] == DepartureAirport[i]:
            if DepartureTime[i] >= ArrivalTime[j] + ServiceTime:
                AdjacencyMatrix[i, j + N] = 1
        else:
            if (ArrivalAirport[j] in TransferDepartureAirport) and (DepartureAirport[i] in TransferArrivalAirport):
                for k in range(TN):
                    if (TransferDepartureAirport[k] == ArrivalAirport[j]) and (
                            TransferArrivalAirport[k] == DepartureAirport[i]):
                        if DepartureTime[i] >= ArrivalTime[j] + 2 * ServiceTime + TransferDuration[k]:
                            AdjacencyMatrix[i, j + N] = 1

for i in range(N):                                # add new sinks, sources and edges to adjacency matrix according to finding circulation algorithm
    AdjacencyMatrix[i, 2 * N] = 1
    AdjacencyMatrix[2 * N + 1, N + i] = 1
    AdjacencyMatrix[2 * N + 1, 2 * N] = 1
    AdjacencyMatrix[i + N, 2 * N + 2] = 1
    AdjacencyMatrix[2 * N, 2 * N + 2] = 1
    AdjacencyMatrix[2 * N + 3, i] = 1
    AdjacencyMatrix[2 * N + 3, 2 * N + 1] = 1

TransfersMatrix = np.zeros(shape=(N, N))         # transfers matrix
for j in range(N):
    for i in range(N):
        TransfersMatrix[j, i] = AdjacencyMatrix[j, i + N]

TransfersQuantity = int(TransfersMatrix.sum())   # number of possible transfers and waitings

capacities = np.ones(shape=int(AdjacencyMatrix.sum())).tolist()         # capacities of the graph, built with the adjacency matrix

for i in range(int(AdjacencyMatrix.sum())):
    capacities[i] = int(capacities[i])

for i in range(N):
    capacities[2 * i] = 0
    capacities[4 * N + int(TransfersQuantity)] = "k"
    capacities[4 * N + int(TransfersQuantity) + 1] = "k"
    capacities[int(AdjacencyMatrix.sum()) - 1] = "k"


file = open("file.txt", "w+")                    # writing results into file
file.write("Adjacency Matrix: \n \n")
file.write(
    str(AdjacencyMatrix).replace("[", "{").replace(".", ",").replace("0,]", "0},").replace(",]", "}").replace(" ", ""))
file.write("\n \nCapacities: \n \n")
file.write(str(capacities).replace("'", "").replace("[", "{").replace("]", "}").replace(" ", ""))

