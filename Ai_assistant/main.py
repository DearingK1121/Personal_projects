def main():
    print("AI Assistant")
    print("Type 'help' to see commands or 'exit' to quit.")

    while True:
        try:
            command = input("> ").strip().lower()
        except EOFError:
            break

        if command in {"", "help"}:
            print("Commands: help, time, joke, exit")
        elif command == "time":
            import datetime
            print(datetime.datetime.now().strftime("%H:%M:%S"))
        elif command == "joke":
            print("Why do programmers prefer dark mode? Because light attracts bugs.")
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
