# Conway's Game of life

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. Also the two-dimensional grid is implemented as a torus (the top row wraps around with the bottom and the left columns with the right). At each step in time, the following transitions occur:

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# Implementation

When the program starts, it generated 20 states as "headroom" for when it generates the next states. State generation is implemented using process pool on multiple cores and it generates a process for each processor core. GUI is on the main thread, while the state generation in on a seperate thread. The states are stored in a queue so when each state is displayed, it is discarded.

# Controls

- Left mouse button - Set cell to alive or dead
- Middle mouse button - Randomly generate start state
- Right mouse button - Starts the simulation



![alt text](https://github.com/gojkovicmatija99/Game-of-life/blob/master/demo.gif)
