"""
Joshua Liu
"""

import pygame
from pygame.draw import line, rect
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
        self.group = -1  # keeps track of its spot in the maze (path generation)
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
                pygame.draw.line(
                    screen, colorList[i], wall[0], wall[1], width=widthList[i]
                )

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

colorList = {0: (255, 255, 255), 1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255)}

BLACK, WHITE, GREEN = (0, 0, 0), (255, 255, 255), (0, 255, 0)

WINDOW_SIZE = 750  # WINDOW_SIZE default 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Prims"), screen.fill(BLACK)

CELL_SIZE = 30  # change this to change the size of the maze BUG at 15
MAZE_DRAW_DELAY = 40  # Speed of which the maze generation is displayed in FPS
PATH_DRAW_DELAY = 15  # Speed of which the path generation is displayed in FPS

widthList = {0: CELL_SIZE // 8, 1: CELL_SIZE // 6, 2: CELL_SIZE // 4, 3: CELL_SIZE // 2}

CELLS_SIZE = WINDOW_SIZE // CELL_SIZE
cells = []  # list to store all the cells

startCell, endCell = None, None

closeWindow = False  # termination flag


initcells = lambda: (
    [
        (
            cells.append([]),
            [
                cells[len(cells) - 1].append(
                    Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
                )
                for x in range(CELLS_SIZE)
            ],
        )
        for y in range(CELLS_SIZE)
    ],
    getCellNeighbours(),
)


# get the left, right, top, and bottom adjacent cells
def getCellNeighbours():
    for cc in cells:
        for c in cc:
            for cc1 in cells:
                for c1 in cc1:
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
    for cc in cells:
        for c in cc:
            c.index = -1
            c.visited = False
    mapSets = {}
    start = 0
    for cell in cells[0]:
        if cell.group == -1:
            cell.group = start
            mapSets.update({start: [cell]})
            start += 1
    for i, cell in enumerate(cells[0]):
        if cell.rightNeighbour is not None and cell.rightNeighbour.group != cell.group:
            if randint(0, 1) == 0:
                cell.wallsToDraw[2] = False
                cell.rightNeighbour.wallsToDraw[0] = False
                mapSets[cell.rightNeighbour.group].remove(cell.rightNeighbour)
                mapSets[cell.group].append(cell.rightNeighbour)
                cell.rightNeighbour.group = cell.group
    for l in range(len(cells) - 1):
        listOfRowGroups = []
        for cell in cells[l]:
            (
                listOfRowGroups.append(cell.group)
                if not listOfRowGroups.__contains__(cell.group)
                else ""
            )
        for group in listOfRowGroups:
            chosenCell = choice(mapSets[group])
            if chosenCell.botNeighbour is not None:
                chosenCell.wallsToDraw[3] = False
                chosenCell.botNeighbour.wallsToDraw[1] = False
                mapSets[chosenCell.group] = []
                mapSets[chosenCell.group].append(chosenCell.botNeighbour)
                chosenCell.botNeighbour.group = chosenCell.group
        for cell in cells[l + 1]:
            if cell.group == -1:
                cell.group = start
                mapSets.update({start: [cell]})
                start += 1
        for cell in cells[l + 1]:
            if cell.rightNeighbour is not None:
                if randint(0, 1) == 0:
                    cell.wallsToDraw[2] = False
                    cell.rightNeighbour.wallsToDraw[0] = False
                    mapSets[cell.rightNeighbour.group].remove(cell.rightNeighbour)
                    mapSets[cell.group].append(cell.rightNeighbour)
                    cell.rightNeighbour.group = cell.group

    mapSets = {}

    for cc in cells:
        for c in cc:
            if not mapSets.keys().__contains__(c.group):
                mapSets.update({c.group: [c]})
            else:
                mapSets[c.group].append(c)

    for cell in cells[len(cells) - 1]:
        if cell.rightNeighbour is not None:
            cell.wallsToDraw[2] = False
            cell.rightNeighbour.wallsToDraw[0] = False
            mapSets[cell.rightNeighbour.group].remove(cell.rightNeighbour)
            mapSets[cell.group].append(cell.rightNeighbour)
            cell.rightNeighbour.group = cell.group

    for row in cells:
        for cell in row:
            if cell.group > -1:
                print(f"{cell.group:3d}", end=" ")
        print()
    print()

    # for key in mapSets.keys():
    #     print(key, len(mapSets[key]))

    while not closeWindow:
        if closeWindow:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWindow = True

        [[cell.drawWalls() for cell in cells[i]] for i in range(len(cells))]
        if closeWindow:
            break
        # clock.tick(0.5)
        pygame.display.update()
