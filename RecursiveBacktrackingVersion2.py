"""
Joshua Liu
2024, April 15
Recursive Backtracking maze generation (looped with new maze) with recursive calls
"""

import pygame
from pygame.draw import circle, line, rect
from random import randint


class Cell:
    def __init__(self, x, y, size) -> None:
        self.size = size  # track the dimensions of a cell
        self.x = x  # x pos of the top left corner of the cell
        self.y = y  # y pos of the top left corner of the cell
        self.center = [x + (size // 2), y + (size // 2)]  # center of the cell
        self.visited = False  # keeps track of whether the cell has been used during generation phase
        self.index = -1  # keeps track of its spot in the maze (path generation)
        self.neighbours = []  # keeps track of its neighbours

    def getNeighbourWithPreviousIndex(self):  # used for path generation
        for n in self.neighbours:
            if n.index == self.index - 1:
                return n

    def randomizeNeighbours(self):
        for _ in range(20):  # used for maze generation (swaps elements pseudo randomly)
            index1 = randint(0, len(self.neighbours) - 1)
            index2 = randint(0, len(self.neighbours) - 1)
            self.neighbours[index1], self.neighbours[index2] = (
                self.neighbours[index2],
                self.neighbours[index1],
            )


pygame.init()

clock = pygame.time.Clock()

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Recursive Backtracking"), screen.fill(BLACK)

CELL_SIZE = 30  # change this to change the size of the maze
MAZE_DRAW_DELAY = 40  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

CELLS_SIZE = WINDOW_SIZE // CELL_SIZE
cells = []  # list to store all the cells

startCell, endCell = None, None

closeWindow = False  # termination flag


def initcells():
    for y in range(CELLS_SIZE):
        for x in range(CELLS_SIZE):
            tempCell = Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
            cells.append(tempCell)  # create a cell object, and store it
    getCellNeighbours()


def getCellNeighbours():  # get the left, right, top, and bottom adjacent cells
    for c in cells:
        for c1 in cells:
            if (
                (c.x == c1.x and c.y == c1.y + CELL_SIZE)
                or (c.x == c1.x and c.y == c1.y - CELL_SIZE)
                or (c.x == c1.x + CELL_SIZE and c.y == c1.y)
                or (c.x == c1.x - CELL_SIZE and c.y == c1.y)
            ):
                c.neighbours.append(c1)


def recCreateMaze(counter, currentCell, endCell, closeWindow):
    currentCell.index = counter
    currentCell.visited = True
    if endCell.index < currentCell.index:
        endCell = currentCell  # Set the end cell to be the one with the highest index
    currentCell.randomizeNeighbours()  # randomize
    for n in currentCell.neighbours:  # Iterate through all neighbours
        for event in pygame.event.get():  # Allows for smooth exit mid generation
            if event.type == pygame.QUIT:
                return endCell, True
        if not n.visited:
            endCell, closeWindow = recCreateMaze(counter + 1, n, endCell, closeWindow)
            if closeWindow:  # Allows for smooth exit mid generation
                return endCell, closeWindow
            rect1 = pygame.Rect(
                n.center[0] - CELL_SIZE // 4,
                n.center[1] - CELL_SIZE // 4,
                CELL_SIZE // 2,
                CELL_SIZE // 2,
            )
            rect(screen, WHITE, rect1)  # Draw the filler rect for the corners
            line(screen, WHITE, currentCell.center, n.center, CELL_SIZE // 2)
            clock.tick(MAZE_DRAW_DELAY)  # main part of the maze
            pygame.display.update()
    return endCell, closeWindow


def recDrawPath(cell, closeWindow):
    for n in cell.neighbours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        if cell.index - 1 != n.index:
            continue
        rect1 = pygame.Rect(
            cell.center[0] - CELL_SIZE // 4,
            cell.center[1] - CELL_SIZE // 4,
            CELL_SIZE // 2,
            CELL_SIZE // 2,
        )
        rect(screen, GREEN, rect1)
        line(screen, GREEN, n.center, cell.center, CELL_SIZE // 2)
        clock.tick(PATH_DRAW_DELAY)
        pygame.display.update()
        closeWindow = recDrawPath(n, closeWindow)
    return closeWindow


if __name__ == "__main__":
    initcells()
    while not closeWindow:
        screen.fill(BLACK)
        for c in cells:
            c.index = -1
            c.visited = False
        startCell = cells[randint(0, len(cells) - 1)]
        endCell = startCell
        endCell, closeWindow = recCreateMaze(1, startCell, endCell, closeWindow)
        if closeWindow:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
        circle(screen, GREEN, startCell.center, CELL_SIZE // 4)
        circle(screen, GREEN, endCell.center, CELL_SIZE // 4)
        closeWindow = recDrawPath(endCell, closeWindow)
        if closeWindow:
            break
        clock.tick(0.5)
        pygame.display.update()
