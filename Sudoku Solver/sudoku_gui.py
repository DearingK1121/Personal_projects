"""Sudoku GUI frontend for the robust solver."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from sudoku_solver import SudokuError, SudokuSolver


class SudokuGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Sudoku Solver")
        self.resizable(False, False)
        self.entries: list[list[tk.Entry]] = []
        self._build_grid()
        self._build_buttons()

    def _build_grid(self) -> None:
        frame = tk.Frame(self, padx=10, pady=10)
        frame.grid(row=0, column=0)

        for row in range(9):
            entry_row: list[tk.Entry] = []
            for col in range(9):
                bg = "white"
                if (row // 3 + col // 3) % 2 == 0:
                    bg = "#f0f0f0"
                entry = tk.Entry(frame, width=2, justify="center", font=("Helvetica", 18), bg=bg)
                entry.grid(row=row, column=col, padx=(1 if col % 3 else 4), pady=(1 if row % 3 else 4))
                entry_row.append(entry)
            self.entries.append(entry_row)

    def _build_buttons(self) -> None:
        button_frame = tk.Frame(self, pady=10)
        button_frame.grid(row=1, column=0)

        solve_button = tk.Button(button_frame, text="Solve", width=12, command=self.solve_puzzle)
        solve_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(button_frame, text="Clear", width=12, command=self.clear_grid)
        clear_button.grid(row=0, column=1, padx=5)

        help_button = tk.Button(button_frame, text="Help", width=12, command=self.show_help)
        help_button.grid(row=0, column=2, padx=5)

    def collect_puzzle_lines(self) -> list[str]:
        lines: list[str] = []
        for row in self.entries:
            row_chars: list[str] = []
            for entry in row:
                value = entry.get().strip()
                if value == "":
                    row_chars.append(".")
                else:
                    row_chars.append(value)
            lines.append("".join(row_chars))
        return lines

    def solve_puzzle(self) -> None:
        try:
            puzzle_lines = self.collect_puzzle_lines()
            grid = SudokuSolver.parse_puzzle(puzzle_lines)
            solver = SudokuSolver(grid)
            solution = solver.solve()
            if solution is None:
                messagebox.showinfo("Sudoku Solver", "No solution exists for the provided puzzle.")
                return
            self._display_solution(solution)
        except SudokuError as exc:
            messagebox.showerror("Sudoku Solver", f"Input error: {exc}")
        except Exception as exc:
            messagebox.showerror("Sudoku Solver", f"Unexpected error: {exc}")

    def _display_solution(self, grid: list[list[int]]) -> None:
        for row_index, row in enumerate(grid):
            for col_index, value in enumerate(row):
                self.entries[row_index][col_index].delete(0, tk.END)
                self.entries[row_index][col_index].insert(0, str(value))

    def clear_grid(self) -> None:
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

    def show_help(self) -> None:
        messagebox.showinfo(
            "How to use",
            "Enter digits 1-9 in each cell and leave blanks empty.\n"
            "Then click Solve to fill the puzzle.\n"
            "Use Clear to reset the board."
        )


def main() -> None:
    app = SudokuGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
