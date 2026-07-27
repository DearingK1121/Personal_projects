def main():
    print("Discord Bot Console")
    print("Type 'hello' or 'exit'.")

    while True:
        try:
            message = input("> ").strip().lower()
        except EOFError:
            break

        if message == "hello":
            print("Hello! I am your bot.")
        elif message == "exit":
            print("Bot offline.")
            break
        else:
            print("I don't understand that message.")


if __name__ == "__main__":
    main()
