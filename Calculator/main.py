# main.py

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from operations import add, subtract, multiply, divide
from history import save_history, show_history
from utils import get_number, print_menu


def run_calculator():
    running = True

    while running:
        print_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = get_number("First number: ")
            num2 = get_number("Second number: ")

            result = add(num1, num2)
            print(f"Answer: {result}")
            save_history(f"{num1} + {num2} = {result}")

        elif choice == "2":
            num1 = get_number("First number: ")
            num2 = get_number("Second number: ")

            result = subtract(num1, num2)
            print(f"Answer: {result}")
            save_history(f"{num1} - {num2} = {result}")

        elif choice == "3":
            num1 = get_number("First number: ")
            num2 = get_number("Second number: ")

            result = multiply(num1, num2)
            print(f"Answer: {result}")
            save_history(f"{num1} * {num2} = {result}")

        elif choice == "4":
            num1 = get_number("First number: ")
            num2 = get_number("Second number: ")

            result = divide(num1, num2)
            print(f"Answer: {result}")
            save_history(f"{num1} / {num2} = {result}")

        elif choice == "5":
            show_history()

        elif choice == "6":
            print("Goodbye!")
            running = False

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    run_calculator()