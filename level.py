from dataclasses import dataclass
from typing import List, Set, Tuple

@dataclass
class Inequality:
    # Row major coords
    high: Tuple[int,int]
    low: Tuple[int,int]

@dataclass
class ParsedLevel:
    grid: List[List[str]]
    inequalities: List[Inequality]

def parseFuFen(fufen: str) -> ParsedLevel:
    lines = []
    inequalities = []
    currentLine = []
    for char in fufen:
        if char == '/':
            lines.append(currentLine)
            currentLine = []
        elif char == "." or char.isdigit():
            currentLine.append(char)
        elif char == "^":
            inequalities.append(Inequality((len(lines), len(currentLine)-1),(len(lines)-1, len(currentLine)-1)))
        elif char == "V":
            inequalities.append(Inequality((len(lines)-1, len(currentLine)-1),(len(lines), len(currentLine)-1)))
        elif char == "<":
            inequalities.append(Inequality((len(lines), len(currentLine)),(len(lines), len(currentLine)-1)))
        elif char == ">":
            inequalities.append(Inequality((len(lines), len(currentLine)-1),(len(lines), len(currentLine))))
    if len(currentLine):
        lines.append(currentLine)

    # assert this is square
    height = len(lines)
    width = len(lines[0])
    for line in lines:
        if len(line) != width:
            raise ValueError("Grid is jagged")
    if width != height:
            raise ValueError("Grid is rectangular")

    #assert all the inequalities are valid indices
    for inequality in inequalities:
        if not (\
            inequality.low[0] in range(height) and \
            inequality.high[0] in range(height) and \
            inequality.low[1] in range(width) and \
            inequality.high[1] in range(width) \
        ):
            raise ValueError(f"Inequality outside of grid {inequality}")
    return ParsedLevel(lines, inequalities)

@dataclass
class WorkingLevel:
    grid: List[List[Set[int]]]
    inequalities: List[Inequality]

    def copy(self):
        return WorkingLevel([[s.copy() for s in row] for row in self.grid], self.inequalities)

def createWorkingLevel(level: ParsedLevel) -> WorkingLevel:
    topValue = len(level.grid[0])
    def possibilitiesForSquare(square):
        if square == '.':
            return set(range(1,topValue+1)) 
        else:
            return set([int(square)])
    return WorkingLevel([[possibilitiesForSquare(square) for square in row] for row in level.grid], level.inequalities)

def printIncompleteWorkingLevel(level: WorkingLevel):
    dimension = len(level.grid)
    charDimension = dimension*4+1
    charGrid = []
    for _ in range(charDimension):
        charGrid.append([" "]*charDimension)

    # paint lines
    for row in range(dimension):
        for col in range(dimension+1): 
            charGrid[row*4] = list("\u251c" + "\u253c".join(["\u2500"*3]*dimension) + "\u2524")
        for subRow in range(3):
            for col in range(dimension+1):
                charGrid[row*4+subRow+1][col*4] = "\u2502"
    charGrid[0] = list("\u250c" + "\u252c".join(["\u2500"*3]*dimension) + "\u2510")
    charGrid[-1] = list("\u2514" + "\u2534".join(["\u2500"*3]*dimension) + "\u2518")

    # paint possibilities
    for row in range(dimension):
        for col in range(dimension):
            for i in range(1, dimension+1):
                if i in level.grid[row][col]:
                    charGrid[row*4+1+(i-1)//3][col*4+1+(i-1)%3] = str(i)

    # paint inequalities
    for inequality in level.inequalities:
        char = ""
        if inequality.high[0] > inequality.low[0]:
            char = "^"
        if inequality.high[0] < inequality.low[0]:
            char = "v"
        if inequality.high[1] > inequality.low[1]:
            char = "<"
        if inequality.high[1] < inequality.low[1]:
            char = ">"
        row = (inequality.high[0] + inequality.low[0])/2
        col = (inequality.high[1] + inequality.low[1])/2
        charGrid[int(row*4)+2][int(col*4)+2] = char
    
    for line in charGrid:
        print("".join(line))

def printCompletedLevel(level: WorkingLevel):
    for line in level.grid:
        print("".join((str(next(iter(square))) for square in line)))
    
def isLevelComplete(level: WorkingLevel):
    for line in level.grid:
        for square in line:
            if len(square) != 1:
                return False
    return True