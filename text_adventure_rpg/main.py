def main():
    print("Text Adventure RPG")
    print("You wake up in a village. Type 'look' or 'quit'.")

    while True:
        try:
            action = input("> ").strip().lower()
        except EOFError:
            break

        if action == "look":
            print("You see a path, a shop, and a forest.")
        elif action == "quit":
            print("You leave the adventure.")
            break
        else:
            print("Unknown action.")


if __name__ == "__main__":
    main()
