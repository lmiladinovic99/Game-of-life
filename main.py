import multiprocessing

import pygame
import numpy as np
from view import startGame

clr_alive = (255, 255, 215)
clr_background = (10, 10, 40)
clr_grid = (30, 30, 60)


def setScreen():
    pygame.init()
    pygame.display.set_caption("John Conway's Game of Life")
    screen = pygame.display.set_mode((n * cellSize, n * cellSize))
    screen.fill(clr_grid)

    for row in range(n):
        for col in range(n):
            rect = pygame.Rect(col * cellSize, row * cellSize, cellSize - 1, cellSize - 1)
            pygame.draw.rect(screen, clr_background, rect)
    pygame.display.update()
    return screen


def updateOneCell(stateRow, stateCol, startState, screen):
    rect = pygame.Rect(stateRow * cellSize, stateCol * cellSize, cellSize - 1, cellSize - 1)
    if startState[stateCol][stateRow] == 1:
        clr = clr_background
    else:
        clr = clr_alive
    pygame.draw.rect(screen, clr, rect)
    startState[stateCol][stateRow] = not startState[stateCol][stateRow]


def updateAllCells(startState, screen, n):
    for row in range(n):
        for col in range(n):
            updateOneCell(row, col, startState, screen)


def setAliveCells(n, cellSize):
    screen = setScreen()
    startState = np.zeros((n, n))
    listening = True
    while listening:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = pygame.mouse.get_pressed()
                if button[0]:
                    stateRow = (event.pos[0] // cellSize)
                    stateCol = (event.pos[1] // cellSize)
                    updateOneCell(stateRow, stateCol, startState, screen)
                    pygame.display.update()
                if button[1]:
                    startState = (np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8)
                    updateAllCells(startState, screen, n)
                    pygame.display.update()
                if button[2]:
                    listening = False
            elif event.type == pygame.QUIT:
                quit()
    startGame(screen, startState, n, cellSize)


if __name__ == '__main__':
    n = 50
    cellSize = 10
    setAliveCells(n, cellSize)
