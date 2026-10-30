import logging
from pathlib import Path


def configure_logging(
    log_dir_name: str = "logs",
    log_file_name: str = "paper_trading_database.log",
    level: int = logging.INFO,
) -> logging.Logger:
    project_root = Path(__file__).resolve().parent
    log_dir = project_root / log_dir_name
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("paper_trading_database")
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_dir / log_file_name, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(file_handler)

    return logger
