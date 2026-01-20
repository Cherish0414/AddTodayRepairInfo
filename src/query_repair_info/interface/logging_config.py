import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(
    log_dir: str, 
    log_file: str = "app.log", 
    log_level: int = logging.INFO, 
    max_bytes: int = 5 * 1024 * 1024, 
    backup_count: int = 5) -> None:
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
    
    file_handler = RotatingFileHandler(
        Path(log_dir) / log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count, 
        encoding='utf-8')
    
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=log_level,
        handlers=[file_handler, console_handler]
    )