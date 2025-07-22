# Futoshiki Solver

This is a fun side project I came up with while playing [futoshiki] on my phone. It can theoretically solve any size of futoshiki board.

## Input

The solver takes the level in a notation I called "FuFen" due to its vague resemblance to chess [FEN notation]. It is a string describing the board's squares row-by-row from top-left to bottom right, with lines delimited by the `/` character.

Each line is a series of squares, which are composed of 

* Either a `.` representing a blank square, or a digit
* Zero or more suffixes describing the inequalities that affect that square

Inequalities are represented with `>`, `<`, `^`, and `V`.

* `>` indicates the square is greater than the square to the right
* `<` indicates the square is less than the square to the right
* `^` indicates the square is greater than the square directly above it
* `V` indicates the square is less than the square directly above it

### Examples

* `.>351./.2.5./.....^/.5.3./.432<.`
* `....7..<.<./.V...3.>..^./..^>.7.9.../..7...<6..^/3V7..V..V.8V9/.^.^3^..^<.7../...3.2.V.<.V/..^.<.8...>./.^..V.6.>..^.`
* `..>.>..<..../.>..>.2V..<../6^...>..>.^.9/9.V.<.V<....2/..>.^....V.^./2.<...V..V.>5/3<.V..>.>.>..8/...V.3.>..V./.>.<...^<.V.V.>.^` 

## Method

The solver works by starting with all squares marked with all possible digits, then whittles away the possibilities by applying these rules:

1. Exclusion: If a square is determined (has only one possibility), remove that possibility from all squares which share its row or column
1. Selection: If a possibility only occurs once in any given row or column, remove all other possibilities from the square which it occurred - selecting any of those other possibilities would result in a row or column that misses that digit
1. Lower-bound: If a square is on the high side of an inequality, remove all possibilities that are equal to or lower than the lowest possibility on the low side of that inequality
1. Upper-bound: If a square is on the low side of an inequality, remove all possibilities that are equal to or greater than the highest possibility on the high side of that inequality

It applies these rules until they can no longer be applied. At that point it's hit a wall, so it must continue the search by "guessing" a possibility to remove from the level and continuing. To avoid making a chain of bad guesses, it tries to solve allowing for 1 guess, then 2, then so on.

## Output

The output is either a grid of numbers representing the solution, or a grid showing where the solver got stuck trying to solve the level

## Limitations

The algorithm can fail if it gets into a state where it can't apply any rules, and there's no single possibility that can be removed which would allow it to start applying rules again. I haven't encountered this scenario yet but maybe it will come up.

While the algorithm can hypothetically solve any size of board, the pretty-printing of all the possibilities only works for boards up to 9x9. This is as high as the regular levels in [futoshiki] go.

YMMV if you decide to solve huge levels or levels with no guaranteed solution. The time complexity is pretty bad because it does a depth-first search if it can't apply any of the rules.

[futoshiki]: https://play.google.com/store/apps/details?id=com.alexuvarov.android.futoshiki&hl=en_US&pli=1
[fen notation]: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation 