"""
Joshua Liu
2024, April 15
Recursive Backtracking maze generation (looped with new maze)
"""

import pygame
from pygame.draw import circle, line, rect
from random import randint


class Cell:
    def __init__(self, x, y, size) -> None:
        self.size = size
        self.x = x
        self.y = y
        self.centerX = x + (size // 2)
        self.centerY = y + (size // 2)
        self.visited = False
        self.index = -1
        self.neighbours = []

    def getNeighbourWithPreviousIndex(self):
        for n in self.neighbours:
            if n.index == self.index - 1:
                return n


pygame.init()

clock = pygame.time.Clock()

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Recursive Backtracking"), screen.fill(BLACK)

CELL_SIZE = 30  # change this to change the size of the maze
MAZE_DRAW_DELAY = 30  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

CELLS_SIZE = WINDOW_SIZE // CELL_SIZE
cells = []

mazeData = []
startCell, endCell = None, None

closeWindow = False


def initcells():
    for y in range(CELLS_SIZE):
        for x in range(CELLS_SIZE):
            tempCell = Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
            cells.append(tempCell)
    getCellNeighbours()


def getCellNeighbours():
    for c in cells:
        for c1 in cells:
            if (
                (c.x == c1.x and c.y == c1.y + CELL_SIZE)
                or (c.x == c1.x and c.y == c1.y - CELL_SIZE)
                or (c.x == c1.x + CELL_SIZE and c.y == c1.y)
                or (c.x == c1.x - CELL_SIZE and c.y == c1.y)
            ):
                c.neighbours.append(c1)


def createMaze():
    mazeData.clear()
    for c in cells:
        c.index = -1
        c.visited = False
    counter = 1
    currentCell = cells[randint(0, len(cells) - 1)]
    currentCell.visited = True
    currentCell.index = counter
    usedCells = []
    usedCells.append(currentCell)
    lineStart = [currentCell.centerX, currentCell.centerY]
    lineEnd = [currentCell.centerX, currentCell.centerY]
    endCell = currentCell
    maxIndex = counter
    startCell = currentCell
    while len(usedCells) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return startCell, endCell, True
        usableCells = []
        for c in usedCells[len(usedCells) - 1].neighbours:
            if not c.visited:
                usableCells.append(c)
        if len(usableCells) != 0:
            counter += 1
            currentCell = usableCells[randint(0, len(usableCells) - 1)]
            currentCell.index = counter
            currentCell.visited = True
            if maxIndex < counter:
                maxIndex = counter
                endCell = currentCell
            lineEnd = [currentCell.centerX, currentCell.centerY]
            usedCells.append(currentCell)
            rect1 = pygame.Rect(
                lineStart[0] - CELL_SIZE // 4,
                lineStart[1] - CELL_SIZE // 4,
                CELL_SIZE // 2,
                CELL_SIZE // 2,
            )
            rect(screen, WHITE, rect1)
            mazeData.append([lineStart, lineEnd, CELL_SIZE // 2, rect1])
            line(screen, WHITE, lineStart, lineEnd, CELL_SIZE // 2)
            lineStart = lineEnd
            clock.tick(MAZE_DRAW_DELAY)
            pygame.display.update()
        else:
            usedCells.remove(usedCells[len(usedCells) - 1])
            if len(usedCells) > 0:
                currentCell = usedCells[len(usedCells) - 1]
                counter = currentCell.index
                lineStart = [currentCell.centerX, currentCell.centerY]
    return startCell, endCell, False


def drawPath():
    path = [endCell]
    while path[len(path) - 1] != startCell:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        path.append(path[len(path) - 1].getNeighbourWithPreviousIndex())

        line(
            screen,
            GREEN,
            (path[len(path) - 1].centerX, path[len(path) - 1].centerY),
            (path[len(path) - 2].centerX, path[len(path) - 2].centerY),
            CELL_SIZE // 2,
        )
        clock.tick(PATH_DRAW_DELAY)
        pygame.display.update()


if __name__ == "__main__":
    initcells()
    while not closeWindow:
        screen.fill(BLACK)
        startCell, endCell, closeWindow = createMaze()
        if closeWindow:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
        for data in mazeData:
            line(screen, WHITE, data[0], data[1], data[2])
            rect(screen, WHITE, data[3])
        circle(screen, GREEN, (startCell.centerX, startCell.centerY), CELL_SIZE // 4)
        circle(screen, GREEN, (endCell.centerX, endCell.centerY), CELL_SIZE // 4)
        if drawPath():
            break
        clock.tick(0.5)
        pygame.display.update()
