from typing import List

from matplotlib.pyplot import connect
from GBM_Constants import GBM_constants
from GBM_Comparator import getAccuracy
from dataManager import Cluster, Connection, Point, loadFromCSV, saveToCSV, visualizeRandomGeometricGraph


def resetCluster(vertices: List[Point]):
    for vertex in vertices:
        vertex.cluster = Cluster.Black


def commonMembersCounter(firstList, secondList):
    counter = 0
    for firstVertex in firstList:
        match = [
            secondVertex for secondVertex in secondList if firstVertex.id == secondVertex.id]
        if(len(match) > 0):
            counter += 1
    return counter


def process(firstConnections: List[Point], secondConnections: List[Point], constants: GBM_constants):
    commonNeighbours = commonMembersCounter(
        firstConnections, secondConnections)
    if (abs(commonNeighbours / constants.n - constants.Es) < abs(commonNeighbours / constants.n - constants.Ed)):
        return True
    else:
        return False


def recoverCluster(vertices: List[Point],  edges: List[Connection], constants: GBM_constants):
    if (len(vertices) <= 0):
        print("error: Any vertices are given")
        return

    V1 = []
    V2 = []

    V1.append(vertices[0])  # fist vertex assign to first cluster

    for i, firstVertex in enumerate(vertices):
        firstConnections = [
            edge.first for edge in edges if edge.second == firstVertex]
        firstConnections.extend(
            [edge.second for edge in edges if edge.first == firstVertex])

        for j, secondVertex in enumerate(vertices, start=i + 1):

            # if Do not have connection
            if len([vertex for vertex in firstConnections if vertex.id == secondVertex.id]) <= 0:
                continue

            # if vertex already assigned
            if len([vertex for vertex in V1 if vertex.id == secondVertex.id]) > 0 or len([vertex for vertex in V2 if vertex.id == secondVertex.id]) > 0:
                continue

            secondConnections = [
                edge.first for edge in edges if edge.second == secondVertex]
            secondConnections.extend(
                [edge.second for edge in edges if edge.first == secondVertex])

            # process
            if process(firstConnections, secondConnections, constants) == True:
                # print("true")
                if len([vertex for vertex in V1 if vertex.id == firstVertex.id]) > 0:
                    V1.append(secondVertex)
                else:
                    V2.append(secondVertex)
            else:
                # print("false")
                if len([vertex for vertex in V1 if vertex.id == firstVertex.id]) > 0:
                    V2.append(secondVertex)
                else:
                    V1.append(secondVertex)

    return V1, V2


# ---- Steps ----
# Params
constants = GBM_constants(0.2, 0.01, 1000)  # rs, rd, n
visualize = False
save = True
compare = True

# Load
vertices = []
V1 = loadFromCSV("V1")
V2 = loadFromCSV("V2")
vertices.extend(V1)
vertices.extend(V2)
edges = loadFromCSV("edges")

V1r, V2r = recoverCluster(vertices, edges, constants)


if visualize:
    visualizeRandomGeometricGraph(V1, V2, edges, "Generated")

if compare:
    print("accuracy (V1 with V1r): " + str(getAccuracy(V1, V1r)))
    print("accuracy (V2 with V2r): " + str(getAccuracy(V2, V2r)))

if save:
    # Save
    saveToCSV("V1_recover", V1r)
    saveToCSV("V2_recover", V2r)
    saveToCSV("edges_recover", edges)
