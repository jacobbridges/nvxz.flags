from pathlib import Path

import aiosqlite


def get_conn():
    """
    Get a connection to the SQLite database.
    """
    data_dir = Path("data").mkdir(exists_ok=True)
    return aiosqlite.connect("data/sqlite.db")
