from GBM_Constants import GBM_constants
from array import array
from typing import List
from dataManager import Cluster, Connection, Point, loadFromCSV, saveToCSV, visualizeRandomGeometricGraph
import random
import math


def generateRandomPoints(amount: int):
    vertices = []
    for i in range(amount):
        angle = random.uniform(0, 1)*(math.pi*2)
        vertices.append(Point(id=i, angle=angle, x=math.cos(angle), y=math.sin(
            angle), cluster=Cluster.Red if (i < amount / 2) else Cluster.Blue))
    return vertices


def addEdgesToGraph(vertices, rs, rd):
    edges = []  # edges
    for i in range(0, len(vertices)-1):
        for j in range(i+1, len(vertices)):
            distanceClockwise = abs(vertices[i].angle - vertices[j].angle)
            distanceCounterclockwise = 2 * math.pi - distanceClockwise
            if vertices[i].cluster.name == vertices[j].cluster.name and (distanceClockwise < (2 * math.pi * rs) or distanceCounterclockwise < (2 * math.pi * rs)):
                edges.append(Connection(first=vertices[i], second=vertices[j]))
            elif vertices[i].cluster.name != vertices[j].cluster.name and (distanceClockwise < (2 * math.pi * rd) or distanceCounterclockwise < (2 * math.pi * rd)):
                edges.append(Connection(first=vertices[i], second=vertices[j]))

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

    return edges


# ---- Steps ----
# Params
constants = GBM_constants(0.2, 0.01, 1000)  # rs, rd, n
load = False
visualize = False
save = True

if load:
    # Load
    vertices = loadFromCSV("vertices")
    edges = loadFromCSV("edges")

else:
    # New
    vertices = generateRandomPoints(constants.n)
    edges = addEdgesToGraph(vertices, constants.Rs, constants.Rd)

if visualize:
    visualizeRandomGeometricGraph(vertices, edges, "Generated")

if save:
    # Save
    saveToCSV("vertices", vertices)
    saveToCSV("edges", edges)
