def clear_logs(file_path) -> None:
    with open(file_path, "w") as file:
        file.write("")
