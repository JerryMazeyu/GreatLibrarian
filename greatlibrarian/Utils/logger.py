import logging
import os
import random
import datetime
import contextlib
import functools
import inspect
from typing import Callable, Type


def generate_name() -> str:
    """Random generate a name.

    Returns:
        str: name
    """
    adjectives = [
        "admiring",
        "adoring",
        "affectionate",
        "agitated",
        "amazing",
        "angry",
        "awesome",
        "blissful",
        "bold",
        "boring",
        "brave",
        "busy",
        "charming",
        "clever",
        "cool",
        "compassionate",
        "competent",
        "confident",
        "crazy",
        "dazzling",
        "determined",
        "distracted",
        "dreamy",
        "eager",
        "ecstatic",
        "elastic",
        "elated",
        "elegant",
        "eloquent",
        "epic",
        "exciting",
        "fervent",
        "festive",
        "flamboyant",
        "focused",
        "friendly",
        "frosty",
        "funny",
        "gallant",
        "gifted",
        "goofy",
        "gracious",
        "happy",
        "hardcore",
        "heuristic",
        "hopeful",
        "hungry",
        "infallible",
        "inspiring",
        "jolly",
        "jovial",
        "keen",
        "kind",
        "laughing",
        "loving",
        "lucid",
        "mystifying",
        "modest",
        "musing",
        "naughty",
        "nervous",
        "nice",
        "nifty",
        "nostalgic",
        "objective",
        "optimistic",
        "peaceful",
        "pedantic",
        "pensive",
        "practical",
        "priceless",
        "quirky",
        "quizzical",
        "relaxed",
        "reverent",
        "romantic",
        "sad",
        "serene",
        "sharp",
        "silly",
        "sleepy",
        "stoic",
        "stupefied",
        "suspicious",
        "tender",
        "thirsty",
        "trusting",
        "unruffled",
        "upbeat",
        "vibrant",
        "vigilant",
        "vigorous",
        "wizardly",
        "wonderful",
        "xenodochial",
        "youthful",
        "zealous",
        "zen",
    ]
    scientists = [
        "albattani",
        "allen",
        "almeida",
        "agnesi",
        "archimedes",
        "ardinghelli",
        "aryabhata",
        "austin",
        "babbage",
        "banach",
        "bardeen",
        "bartik",
        "bassi",
        "beaver",
        "bell",
        "benz",
        "bhabha",
        "bhaskara",
        "blackwell",
        "bohr",
        "booth",
        "borg",
        "bose",
        "boyd",
        "brahmagupta",
        "brattain",
        "brown",
        "carson",
        "chandrasekhar",
        "chatelet",
        "chatterjee",
        "chebyshev",
        "cohen",
        "chaum",
        "clarke",
        "colden",
        "cori",
        "cray",
        "curran",
        "curie",
        "darwin",
        "davinci",
        "dewdney",
        "dhawan",
        "diffie",
        "dijkstra",
        "dirac",
        "driscoll",
        "dubinsky",
        "easley",
        "edison",
        "einstein",
        "elbakyan",
        "elgamal",
        "elion",
        "ellis",
        "engelbart",
        "euclid",
        "euler",
        "faraday",
        "feistel",
        "fermat",
        "fermi",
        "feynman",
        "franklin",
        "gagarin",
        "galileo",
        "galois",
        "ganguly",
        "gates",
        "gauss",
        "germain",
        "golick",
        "goodall",
        "gould",
        "greider",
        "grothendieck",
        "haibt",
        "hamilton",
        "hasse",
        "hawking",
        "hellman",
        "heisenberg",
        "hermann",
        "herschel",
        "hertz",
        "heyrovsky",
        "hodgkin",
        "hofstadter",
        "hoover",
        "hopper",
        "hugle",
        "hypatia",
        "ishizaka",
        "jackson",
        "jang",
        "jennings",
        "jepsen",
        "johnson",
        "joliot",
        "jones",
        "kalam",
        "kapitsa",
        "kare",
        "keldysh",
        "keller",
        "kepler",
        "khayyam",
        "khorana",
        "kilby",
        "kirch",
        "knuth",
        "kowalevski",
        "lalande",
        "lamarr",
        "lamport",
        "leakey",
        "leavitt",
        "lewin",
        "lichterman",
        "liskov",
        "lovelace",
        "lumiere",
        "mahavira",
        "margulis",
        "matsumoto",
        "maxwell",
        "mayer",
        "mccarthy",
        "mcclintock",
        "mclean",
        "mcnulty",
        "mendel",
        "mendeleev",
        "meitner",
        "meninsky",
        "merkle",
        "mestorf",
        "mirzakhani",
        "moore",
        "morse",
        "murdock",
        "neumann",
        "newton",
        "nightingale",
        "nobel",
        "nocard",
        "northcutt",
        "noether",
        "norton",
        "noyce",
        "panini",
        "pare",
        "pascal",
        "pasteur",
        "payne",
        "perlman",
        "pike",
        "poincare",
        "poitras",
        "proskuriakova",
        "ptolemy",
        "raman",
        "ramanujan",
        "ride",
        "montalcini",
        "ritchie",
        "robinson",
        "roentgen",
        "rosalind",
        "rubin",
        "saha",
        "sammet",
        "sanderson",
        "satoshi",
        "shamir",
        "shannon",
        "shaw",
        "shirley",
        "shockley",
        "shtern",
        "sinoussi",
        "snyder",
        "solomon",
        "spence",
        "stonebraker",
        "sutherland",
        "swanson",
        "swartzlander",
        "swirles",
        "taussig",
        "tereshkova",
        "tesla",
        "tharp",
        "thompson",
        "torvalds",
        "tu",
        "turing",
        "varahamihira",
        "vaughan",
        "visvesvaraya",
        "volhard",
        "wescoff",
        "wiles",
        "williams",
        "wilson",
        "wing",
        "wozniak",
        "wright",
        "yalow",
        "yonath",
        "zhukovsky",
    ]
    return f"{random.choice(adjectives)}_{random.choice(scientists)}_{datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S')}"


def generate_name_new(type) -> str:
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{type}_{current_time_str}"


def generate_logger_subfile() -> str:
    subfilenum = "1"
    subfilename = "Test" + subfilenum
    logger_file = os.path.join("Logs", subfilename)

    analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
    dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
    dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    while (
        os.path.exists(logger_file)
        and analyse_exist
        and dialog_exist
        and dialog_init_exist
    ):
        subfilenum = str(int(subfilenum) + 1)
        subfilename = "Test" + subfilenum
        logger_file = os.path.join("Logs", subfilename)

        analyse_exist = os.path.exists(os.path.join(logger_file, "analyse.log"))
        dialog_exist = os.path.exists(os.path.join(logger_file, "dialog.log"))
        dialog_init_exist = os.path.exists(os.path.join(logger_file, "dialog_init.log"))

    return subfilename


def setup_logger(logger_name, logger_file, level=logging.INFO) -> None:
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
            os.path.join(logger_file, f"{logger_name}.log"), mode="a"
        )
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)


def get_logger(logger_name) -> logging.Logger:
    """Get logger instance by name.

    Args:
        logger_name (str): Logger name.

    Returns:
        Logger: Logger instance
    """
    return logging.getLogger(logger_name)


class LoggerWriter:
    """A class for logging purposes that behaves like a file-like object. It can be used to redirect standard output (like the print function) to a logger from Python's logging module.

    Methods
    -------
    write(message: str) -> None:
        Write a message to the logger. If the first word of the message matches
        any logging level name (like 'DEBUG', 'INFO', etc.), the message is formatted
        and logged at that level. Otherwise, the message is logged at the INFO level.

    flush() -> None:
        A placeholder method to provide file-like object behavior. In the context of
        logging, there's generally no need to do anything when flushing output.

    Example
    -------
    >>> import logging
    >>> logger = logging.getLogger('my_logger')
    >>> logger_writer = LoggerWriter(logger)
    >>> print('Hello, world!', file=logger_writer)  # This will log "Hello, world!" at the INFO level.

    Attributes
    ----------
    logger : Logger
        An instance of a logger from Python's logging module.
    """

    def __init__(self, logger) -> None:
        self.logger = logger

    def write(self, message) -> None:
        if message != "\n":
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            level_name, _, msg = message.partition(" ")
            if level_name.upper() in logging._nameToLevel:  # 判断是否为日志等级名称
                formatted_message = f"{now} - {level_name.upper()} - {msg}"
            else:
                formatted_message = f"{now} - INFO - {message}"
            self.logger.info(formatted_message)

    def flush(self) -> None:
        try:
            self.logger.flush()
        except:
            pass


def add_logger(logger_name, logger_file) -> Callable:
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
        logger_name = generate_name()
    if not logger_file:
        logger_file = "Logs"

    if not os.path.exists(logger_file):
        os.makedirs(logger_file)

    def decorate(func):
        setup_logger(logger_name, logger_file)
        logger = logging.getLogger(logger_name)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with contextlib.redirect_stdout(LoggerWriter(logger)):
                return func(*args, **kwargs)

        return wrapper

    return decorate


def add_logger_name_cls(logger_name, logger_file) -> Callable[[Type], Type]:
    def add_logger_to_class(cls):
        """
        A decorator to add logging functionality to all methods of a class.

        This decorator applies the `add_logger` decorator to every method in a class,
        redirecting the standard output of each method to a log file. All methods of
        the class will share the same log file, which is named using a random name
        generated by `generate_name()` function.

        Parameters:
        cls: The class to be decorated.

        Returns:
        The decorated class, with logging functionality added to its methods.

        Example:

        @add_logger_to_class
        class MyClass:
            def method1(self):
                print("Hello from method1!")
            def method2(self):
                print("Hello from method2!")

        # Now all print statements within the methods of MyClass will be logged into the same log file.

        Note: This decorator assumes the existence of a 'Logs' directory in the current working path.
        """
        # logger_name = generate_name()
        setattr(cls, "logger_name", logger_name)
        for attr_name, attr_value in inspect.getmembers(cls):
            if inspect.isfunction(attr_value):
                decorated_func = add_logger(
                    logger_name=logger_name, logger_file=logger_file
                )(attr_value)
                setattr(cls, attr_name, decorated_func)
        return cls

    return add_logger_to_class
