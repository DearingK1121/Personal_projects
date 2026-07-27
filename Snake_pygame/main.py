def main():
    print("Snake Game")
    print("Use WASD to move. Type 'quit' to exit.")

    board = [["." for _ in range(10)] for _ in range(10)]
    snake = [(5, 5)]
    board[5][5] = "S"

    while True:
        for row in board:
            print(" ".join(row))

        try:
            move = input("Move: ").strip().lower()
        except EOFError:
            break

        if move == "quit":
            print("Game over.")
            break

        if move in {"w", "a", "s", "d"}:
            print(f"Snake moved {move}.")
        else:
            print("Use w, a, s, or d.")


if __name__ == "__main__":
    main()
