# Sudoku Solver

A robust Sudoku solver that validates input, detects invalid puzzles, and solves valid puzzles using backtracking.

## Features

- Validates 9x9 grids with integers 0-9
- Supports puzzle input using digits, `0`, or `.` for blank cells
- Detects invalid row/column/box conflicts
- Solves puzzles or reports when unsolvable
- Includes unit tests for correctness

## Usage

Run from the command line:

```sh
python sudoku_solver.py
```

Then enter 9 lines of puzzle input, for example:

```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

Or solve from a file:

```sh
python sudoku_solver.py --file puzzle.txt
```

Run the graphical interface:

```sh
python sudoku_gui.py
```

## Testing

Install `pytest` if needed and run:

```sh
pytest test_sudoku_solver.py
```
