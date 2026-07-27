# This provides the history of the whole calculator

from pathlib import Path

HISTORY_FILE = Path(__file__).with_name("History.txt")


def save_history(entry):
    with HISTORY_FILE.open("a", encoding="utf-8") as file:
        file.write(entry + "\n")


def show_history():
    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            history = file.readlines()
            if len(history) == 0:
                print("\nNo history found.\n")
            else:
                print("\n==== History ====")
                for line in history:
                    print(line.strip())
                print("===================\n")
    except FileNotFoundError:
        print("\nNo history file found.\n")