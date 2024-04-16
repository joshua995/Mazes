"""
Joshua Liu
2024, April 16
Binary Tree maze generation (looped with new maze)
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
        self.right = None
        self.bottom = None


pygame.init()

clock = pygame.time.Clock()

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Binary Tree"), screen.fill(BLACK)

CELL_SIZE = 30  # change this to change the size of the maze
MAZE_DRAW_DELAY = 30  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

CELLS_SIZE = WINDOW_SIZE // CELL_SIZE
cells = []

closeWindow = False  # termination flag


def initcells():
    for y in range(CELLS_SIZE):
        for x in range(CELLS_SIZE):
            tempCell = Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
            cells.append(tempCell)
    getCellNeighbours()


def getCellNeighbours():
    for c in cells:
        for c1 in cells:
            if c.x == c1.x and c.y == c1.y + CELL_SIZE:
                c1.right = c
            elif c.x == c1.x + CELL_SIZE and c.y == c1.y:
                c1.bottom = c


def recCreateMaze(parent, closeWindow):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    if parent is None or parent.visited:
        return
    parent.visited = True
    if not randint(0, 1) and parent.right is not None:
        rect1 = pygame.Rect(
            parent.right.center[0] - CELL_SIZE // 8,
            parent.right.center[1] - CELL_SIZE // 8,
            CELL_SIZE // 4,
            CELL_SIZE // 4,
        )
        rect(screen, WHITE, rect1)
        line(screen, WHITE, parent.right.center, parent.center, CELL_SIZE // 4)
    elif parent.bottom is not None:
        rect1 = pygame.Rect(
            parent.bottom.center[0] - CELL_SIZE // 8,
            parent.bottom.center[1] - CELL_SIZE // 8,
            CELL_SIZE // 4,
            CELL_SIZE // 4,
        )
        rect(screen, WHITE, rect1)
        line(screen, WHITE, parent.bottom.center, parent.center, CELL_SIZE // 4)
    clock.tick(MAZE_DRAW_DELAY)
    pygame.display.update()
    closeWindow = recCreateMaze(parent.right, closeWindow)
    if closeWindow:
        return closeWindow
    closeWindow = recCreateMaze(parent.bottom, closeWindow)
    return closeWindow


if __name__ == "__main__":
    initcells()
    while not closeWindow:
        screen.fill(BLACK)
        for c in cells:
            c.index = -1
            c.visited = False
        closeWindow = recCreateMaze(cells[0], closeWindow)
        if closeWindow:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        pygame.display.update()
