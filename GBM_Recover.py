from typing import List

from matplotlib.pyplot import connect
from GBM_Constants import GBM_constants
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


def recoverCluster(vertices: List[Point], edges: List[Connection], constants: GBM_constants):
    if (len(vertices) <= 0):
        print("error: Any vertices are given")
        return

    vertices[0].cluster = Cluster.Red  # fist vertex assign to first cluster

    for i, firstVertex in enumerate(vertices):
        firstConnections = [
            edge.first for edge in edges if edge.second == firstVertex]
        firstConnections.extend(
            [edge.second for edge in edges if edge.first == firstVertex])

        for j, secondVertex in enumerate(vertices, start=i + 1):
            # if Do not have connection
            if len([vertex for vertex in firstConnections if vertex == secondVertex]) <= 0:
                continue

            if secondVertex.cluster != Cluster.Black:  # if vertex already assigned
                continue

            secondConnections = [
                edge.first for edge in edges if edge.second == secondVertex]
            secondConnections.extend(
                [edge.second for edge in edges if edge.first == secondVertex])

            # process
            if (process(firstConnections, secondConnections, constants) == True):
                secondVertex.cluster = firstVertex.cluster
            elif firstVertex.cluster == Cluster.Red:
                secondVertex.cluster = Cluster.Blue
            elif firstVertex.cluster == Cluster.Blue:
                secondVertex.cluster = Cluster.Red


# ---- Steps ----
# Params
constants = GBM_constants(0.2, 0.01, 1000)  # rs, rd, n
visualize = False
save = True

# Load
vertices = loadFromCSV("vertices")
edges = loadFromCSV("edges")

resetCluster(vertices)
recoverCluster(vertices, edges, constants)

if visualize:
    visualizeRandomGeometricGraph(vertices, edges, "Recovered")

if save:
    # Save
    saveToCSV("vertices_recovered", vertices)
    saveToCSV("edges_recovered", edges)
