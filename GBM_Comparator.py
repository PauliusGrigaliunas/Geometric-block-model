from dataManager import loadFromCSV


def getAccuracy(a, b):
    counter = 0
    for vertexA in a:
        for vertexB in b:
            if vertexA.id == vertexB.id:
                counter += 1
                break

    return  counter/len(a)

