import logging
from typing import ClassVar

from colorama import Fore, Style

LOGGER_MSG_CONFIG = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


class ColoredFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord):
        if record.levelno in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelno]}{record.levelname}{Style.RESET_ALL}"
            )
            record.msg = f"{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}"

        return super().format(record)


def setup_logging(logger_name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(LOGGER_MSG_CONFIG)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
