from pathlib import Path

import aiosqlite


def get_conn():
    """
    Get a connection to the SQLite database.
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return aiosqlite.connect(data_dir / "sqlite.db")
