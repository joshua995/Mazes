"""
Joshua Liu

To many for loops, slow


Start: Choose a random cell on the grid and mark it as part of the maze (visited).
Initialize Frontier: Add all of the unvisited neighboring cells of the starting cell to a list or set called the "frontier".
Iterate: While the frontier list is not empty, repeat the following steps:
Pick a Random Cell: Select a cell at random from the frontier list.
Connect to Maze: Randomly select one of the chosen cell's neighbors that is already in the maze (visited).
Carve Passage: Remove the wall between the random frontier cell and its connected maze neighbor, making a passage.
Mark as Visited: Mark the frontier cell as part of the maze (visited) and remove it from the frontier list.
Update Frontier: Add all of the unvisited neighbors of the newly added cell to the frontier list.
Finish: The process ends when the frontier list is empty and all cells are connected to the main maze structure, ensuring a perfect maze with no loops.
"""

import pygame
from pygame.draw import circle, line, rect
from random import randint, choice


class Cell:
    def __init__(self, x, y, size) -> None:
        self.size = size  # track the dimensions of a cell
        self.x = x  # x pos of the top left corner of the cell
        self.y = y  # y pos of the top left corner of the cell
        self.center = [x + (size // 2), y + (size // 2)]  # center of the cell
        self.visited = False  # keeps track of whether the cell has been used during generation phase
        self.walls = [
            [(x, y), (x, y + size)],  # Left wall
            [(x, y), (x + size, y)],  # Top wall
            [(x + size, y), (x + size, y + size)],  # Right wall
            [(x, y + size), (x + size, y + size)],  # Bot wall
        ]  # pygame line coordinates
        self.wallsToDraw = [True, True, True, True]
        self.index = -1  # keeps track of its spot in the maze (path generation)
        self.leftNeighbour = None
        self.rightNeighbour = None
        self.topNeighbour = None
        self.botNeighbour = None
        self.neighbours = []  # keeps track of its neighbours

    def getNeighbourWithPreviousIndex(self):  # used for path generation
        for n in self.neighbours:
            if n.index == self.index - 1:
                return n

    def drawWalls(self):
        for i, wall in enumerate(self.walls):
            if self.wallsToDraw[i]:
                pygame.draw.line(screen, WHITE, wall[0], wall[1], width=1)

    def expand(self):
        self.visited = True
        visitedNeighbours = []
        for n in self.neighbours:
            if n.visited:
                visitedNeighbours.append(n)
            elif not n.visited and not frontier.__contains__(n):
                frontier.append(n)
        cellToExpand = choice(visitedNeighbours)
        chosenVisited = self.getWhichNeighbour(cellToExpand)
        if chosenVisited == "left":
            self.wallsToDraw[0] = False
            cellToExpand.wallsToDraw[2] = False
        elif chosenVisited == "right":
            self.wallsToDraw[2] = False
            cellToExpand.wallsToDraw[0] = False
        elif chosenVisited == "top":
            self.wallsToDraw[1] = False
            cellToExpand.wallsToDraw[3] = False
        elif chosenVisited == "bot":
            self.wallsToDraw[3] = False
            cellToExpand.wallsToDraw[1] = False

    def getWhichNeighbour(self, cellToCheck):
        if self.leftNeighbour is not None and (
            self.leftNeighbour.x == cellToCheck.x
            and self.leftNeighbour.y == cellToCheck.y
        ):
            return "left"
        elif self.rightNeighbour is not None and (
            self.rightNeighbour.x == cellToCheck.x
            and self.rightNeighbour.y == cellToCheck.y
        ):
            return "right"
        elif self.topNeighbour is not None and (
            self.topNeighbour.x == cellToCheck.x
            and self.topNeighbour.y == cellToCheck.y
        ):
            return "top"
        elif self.botNeighbour is not None and (
            self.botNeighbour.x == cellToCheck.x
            and self.botNeighbour.y == cellToCheck.y
        ):
            return "bot"


pygame.init()

clock = pygame.time.Clock()

colorList = {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255)}
widthList = {0: 1, 1: 5, 2: 10, 3: 15}

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Prims"), screen.fill(BLACK)

CELL_SIZE = 20  # change this to change the size of the maze BUG at 15
MAZE_DRAW_DELAY = 40  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

CELLS_SIZE = WINDOW_SIZE // CELL_SIZE
cells = []  # list to store all the cells

startCell, endCell = None, None

closeWindow = False  # termination flag


initcells = lambda: (
    [
        [
            cells.append(Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE))
            for x in range(CELLS_SIZE)
        ]
        for y in range(CELLS_SIZE)
    ],
    getCellNeighbours(),
)


# get the left, right, top, and bottom adjacent cells
def getCellNeighbours():
    for c in cells:
        for c1 in cells:
            if (
                (top := (c.x == c1.x and c.y == c1.y + CELL_SIZE))
                or (bot := (c.x == c1.x and c.y == c1.y - CELL_SIZE))
                or (left := (c.x == c1.x + CELL_SIZE and c.y == c1.y))
                or (right := (c.x == c1.x - CELL_SIZE and c.y == c1.y))
            ):
                if bot:
                    c.botNeighbour = c1
                elif top:
                    c.topNeighbour = c1
                elif left:
                    c.leftNeighbour = c1
                elif right:
                    c.rightNeighbour = c1
                c.neighbours.append(c1)


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
    for c in cells:
        c.index = -1
        c.visited = False
    startCell = choice(cells)
    startCell.visited = True

    frontier = [n for n in startCell.neighbours if not n.visited]
    while not closeWindow:
        while len(frontier) > 0:
            screen.fill(BLACK)
            chosenCell = choice(frontier)
            chosenCell.expand()
            frontier.remove(chosenCell)
            [cell.drawWalls() for cell in cells]
            clock.tick(60)
            pygame.display.update()

        if closeWindow:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # if len(frontier) > 0:
                #     screen.fill(BLACK)
                #     chosenCell = choice(frontier)
                #     chosenCell.expand()
                #     [
                #         frontier.remove(chosenCell)
                #         for _ in range(frontier.count(chosenCell))
                #     ]
                #     [cell.drawWalls() for cell in cells]
                #     clock.tick(60)
                #     pygame.display.update()

        [cell.drawWalls() for cell in cells]
        if closeWindow:
            break
        # clock.tick(0.5)
        pygame.display.update()
