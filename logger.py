import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logger() -> None:
    log_dir = Path("./server_logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_format = (
        "~ [ %(asctime)s | %(levelname)-8s | "
        "%(name)s | %(message)s ]"
    )

    formatter = logging.Formatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # CONSOLE: INFO и выше
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # FILE: DEBUG и выше
    file_handler = RotatingFileHandler(
        filename=log_dir / "main.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # ROOT LOGGER
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)