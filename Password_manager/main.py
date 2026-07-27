def main():
    passwords = {}
    print("Password Manager")
    print("Commands: add, view, list, exit")

    while True:
        try:
            command = input("> ").strip().lower()
        except EOFError:
            break

        if command == "add":
            site = input("Site: ").strip()
            password = input("Password: ").strip()
            passwords[site] = password
            print("Password saved.")
        elif command == "view":
            site = input("Site: ").strip()
            print(passwords.get(site, "Not found."))
        elif command == "list":
            if passwords:
                for site in passwords:
                    print(f"{site}: {passwords[site]}")
            else:
                print("No passwords saved.")
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
