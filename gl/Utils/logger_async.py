import logging
import os
import random
import datetime
import contextlib
import functools
import inspect
from typing import Callable
import inspect
from functools import partial
import time
import io
import sys
import asyncio
from typing import Callable
from functools import wraps


def generate_name_new(type) -> str:
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{type}_{current_time_str}"


def generate_logger_subfile(Logs_path) -> str:
    subfilenum = "1"
    subfilename = "Test" + subfilenum
    if Logs_path != "":
        logger_file = os.path.join(Logs_path, subfilename)
    else:
        logger_file = os.path.join("Logs", subfilename)

    # analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
    # dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
    # dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    while (
        os.path.exists(logger_file)
        # and analyse_exist
        # and dialog_exist
        # and dialog_init_exist
    ):
        subfilenum = str(int(subfilenum) + 1)
        subfilename = "Test" + subfilenum
        logger_file = os.path.join("Logs", subfilename)

        # analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
        # dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
        # dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    return subfilename


def setup_logger_async(logger_name, logger_file, level=logging.INFO) -> None:
    """Setup logger only if there is no logger.

    Args:
        logger_name (str): Unique name of the logger.
        log_file (str): The path of log, like /xxx/xxx/, don't add the name of logger.
        level (logging.LEVEL, optional): Defaults to logging.INFO.
    """
    l = logging.getLogger(logger_name)
    if not l.handlers:  # Only add handlers if there are none yet
        formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s: %(message)s")

        fileHandler = logging.FileHandler(
            os.path.join(logger_file, f"{logger_name}.log"), mode="a", encoding="utf-8"
        )
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        # streamHandler.setStream(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)


def get_logger_async(logger_name) -> logging.Logger:
    """Get logger instance by name.

    Args:
        logger_name (str): Logger name.

    Returns:
        Logger: Logger instance
    """
    return logging.getLogger(logger_name)





def apply_decorator_to_func_async(decorater, func) -> Callable:
    """
    Apply a given decorator to a function.

    Parameters:
    decorator: The decorator to be applied.
    cls: The function to which the decorator will be applied.
    """
    decorated_function = decorater(func)
    return decorated_function


def setup_async(logger_name, logger_file) -> Callable:
    return partial(add_logger_async, logger_name, logger_file)



class LoggerWriter_async:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f"{now} - {message.rstrip()}")

    def flush(self):
        pass

async def add_logger_async(logger_name=None, logger_file=None) -> callable:
    """A decorator function that adds a logger to the function it decorates.

    This decorator redirects the standard output from the decorated function
    to a file-like logger, allowing the function to log its output with a
    timestamp and a logging level.

    If no logger_name is provided, it generates a random one using `generate_name()`.
    If no logger_file is provided, it creates a log file with the logger_name in the current directory.

    Parameters
    ----------
    logger_name : str, optional
        The name of the logger. If not provided, a random name is generated.
    logger_file : str, optional
        The path where the log file will be created. If not provided, the file is created in
        the current directory with the logger name.

    Example
    -------
    >>> @add_logger(logger_file="Logs")
    ... def my_function():
    ...     print("Debug This is a debug message")
    ...     print("This is an info message")
    >>> my_function()  # This will log the messages with timestamp and level to the specified log file /path/to/log/my_function.log.
    """

    if not logger_name:
        logger_name = generate_name_new()
    if not logger_file:
        logger_file = "Logs"
    await asyncio.sleep(2)
    if not os.path.exists(logger_file):
        os.makedirs(logger_file)

    def decorate(func):
        setup_logger_async(logger_name, logger_file)
        logger = logging.getLogger(logger_name)

        async def wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            sys.stdout = LoggerWriter_async(logger)
            try:
                return await func(*args, **kwargs)
            finally:
                sys.stdout = original_stdout

        return wrapper

    return decorate

async def apply_decorator_to_func_async(decorator, func) -> callable:
    decorated_function = decorator(func)
    return decorated_function
async def setup_async(logger_name, logger_file) -> Callable:
    return await add_logger_async(logger_name, logger_file)