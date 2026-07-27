"""Robust Sudoku solver with validation and command-line support."""

from __future__ import annotations

import argparse
import sys
from copy import deepcopy
from typing import Iterable, List, Optional, Sequence

Grid = List[List[int]]


class SudokuError(ValueError):
    """Exception raised for invalid Sudoku puzzles."""


class SudokuSolver:
    def __init__(self, grid: Grid) -> None:
        self.grid = self._validate_grid(grid)

    @staticmethod
    def _validate_grid(grid: Grid) -> Grid:
        if not isinstance(grid, list) or len(grid) != 9:
            raise SudokuError("Grid must be a 9x9 list of lists.")

        validated: Grid = []
        for row_index, row in enumerate(grid):
            if not isinstance(row, list) or len(row) != 9:
                raise SudokuError("Grid must be a 9x9 list of lists.")
            validated_row: List[int] = []
            for col_index, value in enumerate(row):
                if not isinstance(value, int):
                    raise SudokuError(f"Cell ({row_index + 1},{col_index + 1}) must be an integer.")
                if value < 0 or value > 9:
                    raise SudokuError(f"Cell ({row_index + 1},{col_index + 1}) must be between 0 and 9.")
                validated_row.append(value)
            validated.append(validated_row)

        solver = SudokuSolver.__new__(SudokuSolver)
        solver.grid = validated
        if not solver._grid_is_valid():
            raise SudokuError("Grid contains duplicate values in a row, column, or 3x3 box.")
        return validated

    @staticmethod
    def parse_puzzle(lines: Sequence[str]) -> Grid:
        if len(lines) != 9:
            raise SudokuError("Puzzle input must contain exactly 9 lines.")
        grid: Grid = []
        for line_number, line in enumerate(lines, start=1):
            row = [char for char in line.strip() if char != " "]
            if len(row) != 9:
                raise SudokuError(f"Line {line_number} must contain exactly 9 digits or dots.")
            parsed_row: List[int] = []
            for char in row:
                if char == "." or char == "0":
                    parsed_row.append(0)
                elif char.isdigit() and 1 <= int(char) <= 9:
                    parsed_row.append(int(char))
                else:
                    raise SudokuError(f"Invalid character '{char}' in line {line_number}. Use digits 1-9, 0, or '.'.")
            grid.append(parsed_row)
        return grid

    def _grid_is_valid(self) -> bool:
        for i in range(9):
            if not self._units_are_valid(self.grid[i]):
                return False
            if not self._units_are_valid([self.grid[row][i] for row in range(9)]):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [
                    self.grid[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                if not self._units_are_valid(box):
                    return False
        return True

    @staticmethod
    def _units_are_valid(unit: List[int]) -> bool:
        values = [value for value in unit if value != 0]
        return len(values) == len(set(values))

    def _find_empty_cell(self) -> Optional[tuple[int, int]]:
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def _can_place(self, row: int, col: int, value: int) -> bool:
        if any(self.grid[row][c] == value for c in range(9)):
            return False
        if any(self.grid[r][col] == value for r in range(9)):
            return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def solve(self, limit: int = 1) -> Optional[Grid]:
        solution: Optional[Grid] = None
        counts = 0

        def backtrack() -> bool:
            nonlocal counts, solution
            cell = self._find_empty_cell()
            if cell is None:
                counts += 1
                if counts == 1:
                    solution = deepcopy(self.grid)
                return counts >= limit

            row, col = cell
            for value in range(1, 10):
                if self._can_place(row, col, value):
                    self.grid[row][col] = value
                    if backtrack():
                        if counts >= limit:
                            return True
                    self.grid[row][col] = 0
            return False

        if not self._grid_is_valid():
            raise SudokuError("Puzzle is invalid and cannot be solved.")

        backtrack()
        return solution

    def is_solved(self) -> bool:
        return self._find_empty_cell() is None and self._grid_is_valid()

    def format_grid(self, grid: Optional[Grid] = None) -> str:
        if grid is None:
            grid = self.grid
        lines: list[str] = []
        for row_index, row in enumerate(grid):
            row_str = " ".join(str(value) if value != 0 else "." for value in row)
            lines.append(row_str)
            if row_index in (2, 5):
                lines.append("")
        return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle.")
    parser.add_argument(
        "puzzle",
        nargs="?",
        help="Nine lines of puzzle input or path to a puzzle file.",
    )
    parser.add_argument(
        "--file",
        dest="file",
        help="Path to a text file containing 9 lines of puzzle input.",
    )
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as puzzle_file:
                raw_lines = [line.rstrip("\n") for line in puzzle_file if line.strip() != ""]
        elif args.puzzle:
            raw_lines = args.puzzle.split("\\n")
        else:
            print("Enter 9 lines of puzzle input, using digits, 0, or '.' for blanks:")
            raw_lines = [input().strip() for _ in range(9)]

        grid = SudokuSolver.parse_puzzle(raw_lines)
        solver = SudokuSolver(grid)
        solution = solver.solve()

        if solution is None:
            print("No solution exists for the provided puzzle.")
            return 1

        print("Solved puzzle:")
        print(solver.format_grid(solution))
        return 0
    except SudokuError as exc:
        print(f"Error: {exc}")
        return 2
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 3
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
