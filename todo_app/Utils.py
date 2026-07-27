def confirm(message):
    response = input(f"{message} (y/n): ").strip().lower()
    return response in {"y", "yes"}
