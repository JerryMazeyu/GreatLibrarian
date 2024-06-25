def append_log(source_log_file, destination_log_file):
    try:
        with open(source_log_file, "r", encoding="utf-8") as source_file:
            source_content = source_file.read()

        with open(destination_log_file, "a", encoding="utf-8") as destination_file:
            destination_file.write("\n")
            destination_file.write(source_content)

        print(f"日志内容成功追加到 {destination_log_file}")
    except Exception as e:
        print(f"发生错误: {e}")
