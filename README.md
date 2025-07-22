# Futoshiki Solver

This is a fun side project I came up with while playing [futoshiki] on my phone. It can theoretically solve any size of futoshiki board, though some of the printing stops working after 9x9.

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

It applies these rules until they can no longer be applied. At that point it's hit a wall, so it must continue the search by removing a possibility from the level and trying to continue. It iterates by trying to remove one possibility at a time.

There is a possible weakness here - if the solver can get into a state where no single possibility can be removed to start applying rules again, it will get stuck.

## Output

The output is either a grid of numbers representing the solution, or a grid showing where the solver got stuck trying to solve the level

[futoshiki]: https://play.google.com/store/apps/details?id=com.alexuvarov.android.futoshiki&hl=en_US&pli=1
[fen notation]: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation 