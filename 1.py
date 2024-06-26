import os
def generate_logger_subfile(Logs_path) -> str:
    subfilenum = "1"
    subfilename = "Test" + subfilenum
    if Logs_path == "":
        logger_file = os.path.join("Logs", subfilename)
    else:
        logger_file = os.path.join(Logs_path, subfilename)

    # analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
    # dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
    # dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    while (
        os.path.exists(logger_file)
        # and analyse_exist
        # and dialog_exist
        # and dialog_init_exist
    ):
        log_num = int(subfilenum) + 1
        subfilenum = str(log_num)
        subfilename = "Test" + subfilenum
        if Logs_path == "":
            logger_file = os.path.join("Logs", subfilename)
        else:
            logger_file = os.path.join(Logs_path, subfilename)

        # analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
        # dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
        # dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    return subfilename
logs_path = r"E:\GL实验\GL_Last\GreatLibrarian\log"
logs_path = os.path.join(logs_path, "Logs")
log_path = os.path.join(logs_path, generate_logger_subfile(logs_path))
print(log_path)
