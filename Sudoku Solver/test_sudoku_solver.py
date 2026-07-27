"""Unit tests for the Sudoku solver."""

from sudoku_solver import SudokuError, SudokuSolver


def test_parse_valid_puzzle() -> None:
    puzzle_lines = [
        "530070000",
        "600195000",
        "098000060",
        "800060003",
        "400803001",
        "700020006",
        "060000280",
        "000419005",
        "000080079",
    ]
    grid = SudokuSolver.parse_puzzle(puzzle_lines)
    solver = SudokuSolver(grid)
    solution = solver.solve()

    assert solution is not None
    assert solver.is_solved()
    assert solution[0][2] == 4
    assert solution[8][7] == 7


def test_invalid_puzzle_duplicate() -> None:
    invalid_lines = [
        "530070000",
        "600195000",
        "098000060",
        "800060003",
        "400803001",
        "700020006",
        "060000280",
        "000419005",
        "000080079",
    ]
    invalid_lines[0] = "530570000"
    try:
        grid = SudokuSolver.parse_puzzle(invalid_lines)
        SudokuSolver(grid)
        assert False, "Expected SudokuError due to duplicate value"
    except SudokuError:
        assert True


def test_unsolvable_puzzle() -> None:
    unsolvable_lines = [
        "530070000",
        "600195000",
        "098000060",
        "800060003",
        "400803001",
        "700020006",
        "060000280",
        "000419005",
        "000080070",
    ]
    grid = SudokuSolver.parse_puzzle(unsolvable_lines)
    solver = SudokuSolver(grid)
    assert solver.solve() is None


def test_complete_puzzle_is_valid() -> None:
    complete_lines = [
        "534678912",
        "672195348",
        "198342567",
        "859761423",
        "426853791",
        "713924856",
        "961537284",
        "287419635",
        "345286179",
    ]
    grid = SudokuSolver.parse_puzzle(complete_lines)
    solver = SudokuSolver(grid)
    assert solver.is_solved()
    assert solver.solve() == grid
