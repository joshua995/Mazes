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
from pygame.draw import line, rect, circle
from random import choice


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

    drawWalls = lambda self: [
        pygame.draw.line(screen, colorList[i], wall[0], wall[1], width=widthList[i])
        for i, wall in enumerate(self.walls)
        if self.wallsToDraw[i]
    ]

    def expand(self):
        self.visited = True
        visitedNeighbours = []
        [
            (
                visitedNeighbours.append(n)
                if n.visited
                else (
                    frontier.append(n)
                    if not n.visited and not frontier.__contains__(n)
                    else ""
                )
            )
            for n in self.neighbours
        ]

        cellToExpand = choice(visitedNeighbours)
        chosenVisited = self.getWhichNeighbour(cellToExpand)
        (
            self.undrawWalls(cellToExpand, 0, 2, False)
            if chosenVisited == "left"
            else (
                self.undrawWalls(cellToExpand, 2, 0, False)
                if chosenVisited == "right"
                else (
                    self.undrawWalls(cellToExpand, 1, 3, False)
                    if chosenVisited == "top"
                    else (
                        self.undrawWalls(cellToExpand, 3, 1, False)
                        if chosenVisited == "bot"
                        else ""
                    )
                )
            )
        )

    def undrawWalls(self, otherCell, selfIndex, otherIndex, bool):
        self.wallsToDraw[selfIndex] = bool
        otherCell.wallsToDraw[otherIndex] = bool

    getWhichNeighbour = lambda self, cellToCheck: (
        "left"
        if self.leftNeighbour is not None
        and (
            self.leftNeighbour.x == cellToCheck.x
            and self.leftNeighbour.y == cellToCheck.y
        )
        else (
            "right"
            if self.rightNeighbour is not None
            and (
                self.rightNeighbour.x == cellToCheck.x
                and self.rightNeighbour.y == cellToCheck.y
            )
            else (
                "top"
                if self.topNeighbour is not None
                and (
                    self.topNeighbour.x == cellToCheck.x
                    and self.topNeighbour.y == cellToCheck.y
                )
                else (
                    "bot"
                    if self.botNeighbour is not None
                    and (
                        self.botNeighbour.x == cellToCheck.x
                        and self.botNeighbour.y == cellToCheck.y
                    )
                    else ""
                )
            )
        )
    )


pygame.init()

clock = pygame.time.Clock()

colorList = {0: (255, 255, 255), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255)}

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Prims"), screen.fill(BLACK)

CELL_SIZE = 10  # change this to change the size of the maze BUG at 15
MAZE_DRAW_DELAY = 40  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

widthList = {0: CELL_SIZE // 8, 1: CELL_SIZE // 6, 2: CELL_SIZE // 4, 3: CELL_SIZE // 2}

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


if __name__ == "__main__":
    initcells()
    # for c in cells:
    #     c.index = -1
    #     c.visited = False
    startCell = choice(cells)
    startCell.visited = True
    endCell = choice(cells)

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
        circle(
            screen, GREEN, (startCell.center[0], startCell.center[1]), CELL_SIZE // 4
        )
        circle(screen, GREEN, (endCell.center[0], endCell.center[1]), CELL_SIZE // 4)
        if closeWindow:
            break
        # clock.tick(0.5)
        pygame.display.update()
