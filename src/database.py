from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "transporte.db"

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco não encontrado: {DB_PATH}")
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

def query_one(sql, params=()):
    with get_connection() as conn:
        row = conn.execute(sql, params).fetchone()
        return None if row is None else row[0]

def query_rows(sql, params=()):
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()
