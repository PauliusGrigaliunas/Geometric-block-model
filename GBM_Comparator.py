from dataManager import loadFromCSV


def getAccuracy():
    createdVertices = loadFromCSV("vertices")
    recoveredVertices = loadFromCSV("vertices_recovered")

    if len(createdVertices) != len(recoveredVertices) or len(createdVertices) == 0:
        print("Error: vertices sizes are diffrent from data sets!")
        return

    counter = 0
    for createdVertex in createdVertices:
        recovered = [
            recoveredVertex for recoveredVertex in recoveredVertices if recoveredVertex.id == createdVertex.id]
        if (createdVertex.cluster == recovered[0].cluster):
            counter += 1

    return counter / len(createdVertices)


print("accuracy: " + str(getAccuracy()))
