from enum import Enum, auto
from typing import List
import pandas as pd
import itertools
from matplotlib import collections, colors
from matplotlib.markers import MarkerStyle
import matplotlib.pyplot as plt


class Cluster(Enum):
    Black = 0  # unassigned
    Red = auto()
    Blue = auto()


class Point:
    def __init__(self, id: int, angle: float, x: float, y: float, cluster: Cluster):
        self.id = id
        self.angle = angle
        self.x = x
        self.y = y
        self.cluster = cluster


class Connection:
    def __init__(self, first: Point, second: Point):
        self.first = first
        self.second = second


vertices = []


def saveToCSV(name: str, dataList: List):
    if len(dataList) > 0:
        if (list(vars(dataList[0]).keys())[0] == "id"):
            df = pd.DataFrame([[data.id, data.angle, data.x, data.y, 1 if data.cluster.name ==
                              "Red" else 2 if data.cluster.name == "Blue" else 0] for data in dataList])
        else:
            df = pd.DataFrame([[data.first.id, data.second.id]
                              for data in dataList])
        df.to_csv(name + '.csv',
                  header=list(vars(dataList[0]).keys()), index=False)
    else:
        return


def loadFromCSV(verticesName: str):
    newData = pd.read_csv(verticesName + '.csv')
    elements = []
    header = list(vars(newData.columns)['_data'])
    if (header == ['id', 'angle', 'x', 'y', 'cluster']):
        for line in newData.values:
            elements.append(
                Point(id=line[0], angle=line[1], x=line[2], y=line[3], cluster=Cluster(line[4])))
        global vertices
        vertices = elements
        return elements
    elif (header == ['first', 'second']):
        for line in newData.values:
            elements.append(Connection(first=[vertex for vertex in vertices if vertex.id == int(
                line[0])][0], second=[vertex for vertex in vertices if vertex.id == int(line[1])][0]))
        return elements

    else:
        return []


def visualizeRandomGeometricGraph(vertices: List[Point], edges: List[Connection], pictureName):
    x = [v.x for v in vertices]
    y = [v.y for v in vertices]
    colors = [v.cluster.name for v in vertices]

    # draw dashed circle
    circle = plt.Circle((0, 0), 1, color='black',
                        linestyle='dashed', fill=False)
    fig, ax = plt.subplots()
    ax.add_patch(circle)

    plt.title('Geometric Block Model ')
    plt.scatter(x, y, s=100, c=colors, edgecolors='black',
                linewidths=1, alpha=0.75)

    for edge in edges:
        plt.plot([edge.first.x, edge.second.x], [
                 edge.first.y, edge.second.y], c='green')

    plt.show()
    fig.savefig(pictureName + '.png')
