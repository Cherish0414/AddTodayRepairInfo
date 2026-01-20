import pyodbc
from contextlib import contextmanager
from ..config.config import config
import logging

logger = logging.getLogger(__name__)

@contextmanager
def db_connection():
    cfg = config.database
    
    conn_str = (
        f"DRIVER={cfg.get('driver', '{ODBC Driver 17 for SQL Server}')};"
        f"SERVER={cfg.get('host', 'localhost')};"
        f"PORT={cfg.get('port', 1433)};"
        f"DATABASE={cfg.get('database', 'unknown_database')};"
        f"UID={cfg.get('username', 'sa')};"
        f"PWD={cfg.get('password', 'your_password')};"
        f"TIMEOUT={cfg.get('timeout', 30)};"
    )
    conn = pyodbc.connect(conn_str)
    try:
        yield conn
        logger.info("Database connection established successfully.")
    finally:
        conn.close()
        