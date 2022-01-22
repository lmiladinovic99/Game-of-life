import time
import queue
import pygame
import threading
from arrayqueues.shared_arrays import ArrayQueue
from model import stateGenerator

clr_alive = (255, 255, 215)
clr_background = (10, 10, 40)
clr_grid = (30, 30, 60)

lock = threading.Lock()
queue = ArrayQueue(100)
lastState = None


def fillQueue(n, goToInfinity):
    global lastState
    global queue
    while True:
        newSteps = stateGenerator(lastState, n, 20)
        for i in range(1, len(newSteps)):
            queue.put(newSteps[i])
        lastState = newSteps[len(newSteps) - 1]
        if not goToInfinity:
            break


def update(screen, currState, n, sz):
    for row in range(n):
        for col in range(n):
            if currState[row, col] == 1:
                clr = clr_alive
            else:
                clr = clr_background
            rect = pygame.Rect(col * sz, row * sz, sz - 1, sz - 1)
            pygame.draw.rect(screen, clr, rect)


def startGame(screen, startState, n, cellSize):
    global lastState
    lastState = startState
    fillQueue(n, False)

    thread = threading.Thread(target=fillQueue, args=(n, True))
    thread.start()

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill(clr_grid)
        currState = queue.get()
        update(screen, currState, n, cellSize)
        pygame.display.update()
        time.sleep(0.08)

    print("Can't calculate that fast!")