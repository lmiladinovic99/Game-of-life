import multiprocessing
import math
import ctypes
import numpy as np

cellsPerPart = 0
n_ = 0
shared_array = None


def updateCurrPart(partNum):
    global cellsPerPart
    global n_
    startCell = partNum * cellsPerPart
    numOfSetCells = 0
    rowColStat = []
    for num in range(startCell, n_ ** 2):
        row = math.floor(num // n_)
        col = num % n_
        alive = 0
        for neighbourRow in range(3):
            for neighbourCol in range(3):
                if neighbourRow == 1 and neighbourCol == 1:
                    continue
                curr = row + neighbourRow - 1
                currNeighbourRow = ((curr % n_) + n_) % n_
                curr = col + neighbourCol - 1
                currNeighbourCol = ((curr % n_) + n_) % n_
                if shared_array[currNeighbourRow, currNeighbourCol] == 1:
                    alive += 1
        status = 0
        if alive < 2 or alive > 3:
            status = 0
        if shared_array[row, col] == 1 and 2 <= alive <= 3:
            status = 1
        if shared_array[row, col] == 0 and alive == 3:
            status = 1
        rowColStat.append([row, col, status])
        numOfSetCells += 1
        if numOfSetCells == cellsPerPart - 1:
            return rowColStat
    return rowColStat


def stateGenerator(startState, n, iterations):
    global shared_array
    global cellsPerPart
    global n_
    listOfMatrix = []
    n_ = n
    numOfParts = multiprocessing.cpu_count()
    shared_array_base = multiprocessing.Array(ctypes.c_double, n ** 2)
    shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
    shared_array = shared_array.reshape(n, n)

    cellsPerPart = math.ceil(n ** 2 / numOfParts)
    pool = multiprocessing.Pool(numOfParts)
    listOfMatrix.append(startState.copy())
    for iter in range(iterations):
        for row in range(n):
            for col in range(n):
                shared_array[row, col] = startState[row, col]
        result = pool.map(updateCurrPart, range(numOfParts))
        for resultSubset in result:
            for cell in resultSubset:
                startState[cell[0], cell[1]] = cell[2]
        listOfMatrix.append(startState.copy())
    pool.close()
    pool.join()
    return listOfMatrix
