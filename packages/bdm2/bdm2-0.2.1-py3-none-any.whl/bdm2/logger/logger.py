import sys
from datetime import datetime
from pathlib import Path

from loguru import logger


def build_logger(file_name, save_log=True):
    logger.remove()
    curr_time = datetime.now()
    curr_time = str(curr_time).replace(":", ".")

    if save_log:
        log_fname = (
                Path(__file__).parent
                / "logs"
                / f"{str(Path(file_name).name).replace('.py', '')}_{curr_time}.txt"
        )
        logger.add(str(log_fname), rotation="500 MB", level="DEBUG")

    logger.add(sys.stdout, level="DEBUG")

    return logger


def log_with_color(message, level):
    color_codes = {
        "TRACE": "\033[34m",  # Blue
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "SUCCESS": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "reset": "\033[0m",
    }
    colored_message = f"{color_codes[level]}{message}{color_codes['reset']}"
    if level == "TRACE":
        logger.trace(colored_message)
    elif level == "DEBUG":
        logger.debug(colored_message)
    elif level == "INFO":
        logger.info(colored_message)
    elif level == "SUCCESS":
        logger.success(colored_message)
    elif level == "WARNING":
        logger.warning(colored_message)
    elif level == "ERROR":
        logger.error(colored_message)
    elif level == "CRITICAL":
        logger.critical(colored_message)

# Примеры записи логов
# logger.debug("Это отладочное сообщение")
# logger.info("Это информационное сообщение")
# logger.warning("Это предупреждение")
# logger.error("Это сообщение об ошибке")
# logger.critical("Это критическая ошибка")

# Настройка конфигурации логгера
