from Storage import save_tasks, load_tasks
from task import Task


class TodoManager:
    def __init__(self, storage_path="tasks.json"):
        self.storage_path = storage_path
        self.tasks = load_tasks(self.storage_path)

    def list_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
            return

        for index, task in enumerate(self.tasks, start=1):
            status = "done" if task.completed else "pending"
            print(f"{index}. {task.title} [{status}]")

    def add_task(self, title):
        if not title:
            print("Task title cannot be empty.")
            return

        task = Task(title)
        self.tasks.append(task)
        save_tasks(self.tasks, self.storage_path)
        print("Task added.")

    def complete_task(self, index):
        if not self._valid_index(index):
            print("Invalid task number.")
            return

        task = self.tasks[index - 1]
        task.completed = True
        save_tasks(self.tasks, self.storage_path)
        print("Task completed.")

    def delete_task(self, index):
        if not self._valid_index(index):
            print("Invalid task number.")
            return

        del self.tasks[index - 1]
        save_tasks(self.tasks, self.storage_path)
        print("Task deleted.")

    def _valid_index(self, index):
        return 1 <= index <= len(self.tasks)
