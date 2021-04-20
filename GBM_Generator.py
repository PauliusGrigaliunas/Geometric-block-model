from GBM_Constants import GBM_constants
from array import array
from typing import List
from dataManager import Cluster, Connection, Point, loadFromCSV, saveToCSV, visualizeRandomGeometricGraph
import random
import math


def generateRandomPoints(amount: int):
    V1 = []
    V2 = []
    for i in range(amount):
        angle = random.uniform(0, 1)*(math.pi*2)
        vertex = Point(id=i, angle=angle, x=math.cos(angle), y=math.sin(
            angle))
        V1.append(vertex) if (i < amount / 2) else V2.append(vertex)
    return V1, V2


def addEdgesFromSameCluster(vertices, rs):
    edges = []
    for i in range(0, len(vertices)-1):
        for j in range(i+1, len(vertices)):
            distanceClockwise = abs(vertices[i].angle - vertices[j].angle)
            distanceCounterclockwise = 2 * math.pi - distanceClockwise
            if (distanceClockwise < (2 * math.pi * rs) or distanceCounterclockwise < (2 * math.pi * rs)):
                edges.append(Connection(first=vertices[i], second=vertices[j]))
    return edges


def addEdgesFromDifferentCluster(V1, V2, rd):
    edges = []

    for vertex1 in V1:
        for vertex2 in V2:
            distanceClockwise = abs(vertex1.angle - vertex2.angle)
            distanceCounterclockwise = 2 * math.pi - distanceClockwise
            if (distanceClockwise < (2 * math.pi * rd) or distanceCounterclockwise < (2 * math.pi * rd)):
                edges.append(Connection(first=vertex1, second=vertex2))
    return edges


def checkIsGraphIsFullyConnected(vertices, edges):
    connectedVertices = []
    connectedVertices.append(vertices[0])
    for vertex in connectedVertices:
        for edge in edges:
            if (edge.first == vertex and not(edge.second in connectedVertices)):
                connectedVertices.append(edge.second)
            if (edge.second == vertex and not(edge.first in connectedVertices)):
                connectedVertices.append(edge.first)

    if len(connectedVertices) != len(vertices):
        print("Error: The graph is not fully connected!")


def addEdgesToGraph(V1, V2, rs, rd):
    edges = []  # edges
    edges.extend(addEdgesFromSameCluster(V1, rs))
    edges.extend(addEdgesFromSameCluster(V2, rs))
    edges.extend(addEdgesFromDifferentCluster(V1, V2, rd))

    vertices = []
    vertices.extend(V1)
    vertices.extend(V2)
    checkIsGraphIsFullyConnected(vertices, edges)

    return edges


# ---- Steps ----
# Params
constants = GBM_constants(0.2, 0.01, 1000)  # rs, rd, n
load = False
visualize = False
save = True

if load:
    # Load
    V1 = loadFromCSV("V1")
    V2 = loadFromCSV("V2")
    edges = loadFromCSV("edges")

else:
    # New
    V1, V2 = generateRandomPoints(constants.n)
    edges = addEdgesToGraph(V1, V2, constants.Rs, constants.Rd)

if visualize:
    visualizeRandomGeometricGraph(V1, V2, edges, "Generated")

if save:
    # Save
    saveToCSV("V1", V1)
    saveToCSV("V2", V2)
    saveToCSV("edges", edges)
