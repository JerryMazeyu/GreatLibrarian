import os
import subprocess
import shlex
import logging


class VirtualEnvRunner:
    def __init__(self, env_name, env_path):
        self.env_name = env_name
        self.env_path = env_path
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # 创建一个文件处理程序，将日志记录到文件中
        log_file = os.path.join(self.env_path, "virtualenv_runner.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # 创建一个控制台处理程序，将日志输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 创建一个格式器，规定日志的输出格式
        formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 将处理程序添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def create_virtualenv(self):
        if not os.path.exists(self.env_path):
            try:
                command = f"python -m venv {self.env_path}"
                args = shlex.split(command)
                subprocess.run(args, check=True, capture_output=True, text=True)
                print(f"Virtual environment {self.env_name} created successfully.")
                print(f"Virtual encironment path: {os.path.abspath(self.env_path)}")
            except subprocess.CalledProcessError as e:
                print("Error creating virtual environment: {e}")
        else:
            print(
                f"Virtual environment {self.env_name} already exists at {os.path.abspath(self.env_path)}."
            )

    def run_code_in_virtualenv(self, code):
        try:
            # Activate the virtual environment
            activate_script = os.path.join(self.env_path, "bin", "activate")
            # activate_cmd = f'bash -i -c "source {activate_script}"'
            command = [activate_script, "&&", "python", "-c", code]

            # Run user input code
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
            )

            self.logger.info("Output:")
            self.logger.info(result.stdout)
            self.logger.error("Error:")
            self.logger.error(result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Unable to run code in your virtual environment:{e}")
            # print('Error running code in virtual environment.')


# Example usage:
if __name__ == "__main__":
    env_name = "my_virtualenv"
    env_path = "/home/ubuntu/moe/GreatLibrarian/greatlibrarian/Agents/CodeRunner/VirEnv"
    code_to_run = input("Enter Python code to run: ")

    runner = VirtualEnvRunner(env_name, env_path)
    runner.create_virtualenv()
    runner.run_code_in_virtualenv(code_to_run)
