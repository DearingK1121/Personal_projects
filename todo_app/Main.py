from Manager import TodoManager


def main():
    manager = TodoManager()
    print("Todo App")
    print("1. View tasks")
    print("2. Add task")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Exit")

    while True:
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nGoodbye!")
            break

        if choice == "1":
            manager.list_tasks()
        elif choice == "2":
            task_text = input("Task: ").strip()
            manager.add_task(task_text)
        elif choice == "3":
            try:
                index = int(input("Task number to complete: ").strip())
                manager.complete_task(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            try:
                index = int(input("Task number to delete: ").strip())
                manager.delete_task(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
