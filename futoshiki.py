from itertools import count
from typing import Optional
from level import *

def rowsAndCols(level: WorkingLevel):
    for row in level.grid:
        yield row
    dimension = len(level.grid)
    for col in range(dimension):
        yield [level.grid[row][col] for row in range(dimension)]

def isLevelValid(level: WorkingLevel) -> bool:
    for rowCol in rowsAndCols(level):
        determined = set()
        possibilities = { num: 0 for num in range(1, len(level.grid)+1)}
        for square in rowCol:
            if len(square) == 0:
                return False
            if len(square) == 1:
                determined.add(next(iter(square)))
            for num in square:
                possibilities[num] += 1
        for num, poss in possibilities.items():
            if poss == 0:
                return False
            if poss > 1 and num in determined:
                return False
    for inequality in level.inequalities:
        lowSquare = level.grid[inequality.low[0]][inequality.low[1]]
        highSquare = level.grid[inequality.high[0]][inequality.high[1]]
        if len(lowSquare) == 1 and len(highSquare) == 1:
            if next(iter(lowSquare)) >= next(iter(highSquare)):
                return False
    return True

##
# No row or column can have a duplicate of a number
# Remove possibilities that suggest this
##
def applyExclusionRule(level: WorkingLevel) -> bool:
    didChange = False
    for rowCol in rowsAndCols(level):
        determined = [next(iter(square)) for square in rowCol if len(square) == 1]
        for square in rowCol:
            if len(square) == 1:
                continue
            for value in determined:
                if value in square:
                    square.discard(value)
                    didChange = True
    return didChange

##
# Each row or column must have at least one occurrence of a number
# If a row or column has only one way of containing that number, that must be the way toward the solution
##
def applySelectionRule(level: WorkingLevel) -> bool:
    didChange = False
    topNum = len(level.grid[0])
    #row wise
    for rowCol in rowsAndCols(level):
        possibilityCount = { num : 0 for num in range(1, topNum+1)}
        for square in rowCol:
            for possibility in square:
                possibilityCount[possibility] += 1
        for possibility, count in possibilityCount.items():
            if count != 1:
                continue
            for square in rowCol:
                if possibility in square and len(square) > 1:
                    didChange = True
                    square.clear()
                    square.add(possibility)
    return didChange

##
# Inequality rule part 1:
# The lowest possibility on the low side of an inequality must be lower than
# the lowest possibility on the high side of the inequality
##
def applyLowerBoundRule(level: WorkingLevel) -> bool:
    didChange = False
    for inequality in level.inequalities:
        lowSquare = level.grid[inequality.low[0]][inequality.low[1]]
        highSquare = level.grid[inequality.high[0]][inequality.high[1]]
        if len(lowSquare) == 0:
            continue
        for lowNum in range(1,min(lowSquare)+1):
            # remove all from the high square which are <= the minimum of the low square
            if lowNum in highSquare:
                highSquare.discard(lowNum)
                didChange = True
    return didChange

##
# Inequality rule part 2:
# The highest possibility on the high side of an inequality must be higher than
# the highest possibility on the low side of the inequality
##
def applyUpperBoundRule(level: WorkingLevel):
    didChange = False
    topNum = len(level.grid[0])
    for inequality in level.inequalities:
        lowSquare = level.grid[inequality.low[0]][inequality.low[1]]
        highSquare = level.grid[inequality.high[0]][inequality.high[1]]
        if len(highSquare) == 0:
            continue
        for highNum in range(max(highSquare),topNum+1):
            #remove all from the high square which are <= the minimum of the low square
            if highNum in lowSquare:
                lowSquare.discard(highNum)
                didChange = True
    return didChange

def applyRules(workingLevel: WorkingLevel):
    return \
        applyExclusionRule(workingLevel) or \
        applyLowerBoundRule(workingLevel) or \
        applyUpperBoundRule(workingLevel) or \
        applySelectionRule(workingLevel)

# Generates versions of the level with a single possibility removed
def validMutations(workingLevel: WorkingLevel):
    for row in range(len(workingLevel.grid)):
        for col in range(len(workingLevel.grid)):
            for num in range(1, len(workingLevel.grid)+1):
                if num not in workingLevel.grid[row][col]:
                    continue
                nextIteration = workingLevel.copy()
                nextIteration.grid[row][col].discard(num)
                if isLevelValid(nextIteration):
                    yield nextIteration

def solveWorkingLevel(workingLevel: WorkingLevel, maxDepth: int, depth: int = 1) -> bool:
    print("Solving, depth = ", depth, "maxDepth = ", maxDepth)
    appliedAnyRules = False
    while applyRules(workingLevel):
        # applyRules affects workingLevel and
        # returns false when no rules apply
        appliedAnyRules = True
    if not appliedAnyRules:
        return False
    if not isLevelValid(workingLevel):
        return False
    if isLevelComplete(workingLevel):
        return True

    # Here, we've reached a state where our rules can't advance us
    # further, so make a random mutation and try to keep solving
    if depth < maxDepth:
        for nextIteration in validMutations(workingLevel):
            if solveWorkingLevel(nextIteration, maxDepth, depth+1):
                workingLevel.grid = nextIteration.grid
                return True
    return False


print("Enter level in fufen notation")
fufen = input()
level = parseFuFen(fufen)
print("Parsed Level:")
workingLevel = createWorkingLevel(level)
print()

# Gradually descend, allowing for more guesses each time
for depth in range(1, 20):
    solveWorkingLevel(workingLevel, depth)

print("Solution:")
printCompletedLevel(workingLevel)