import json
from pathlib import Path


def load_tasks(storage_path="tasks.json"):
    path = Path(storage_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            raw = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    from task import Task

    return [Task(item["title"], item.get("completed", False)) for item in raw]


def save_tasks(tasks, storage_path="tasks.json"):
    path = Path(storage_path)
    payload = [{"title": task.title, "completed": task.completed} for task in tasks]

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
