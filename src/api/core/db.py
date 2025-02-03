from pathlib import Path

import aiosqlite


class AutoFKConnection:
    def __init__(self, cnxn_path):
        self.cnxn_path = cnxn_path
        self.conn = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.cnxn_path)
        await self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


def get_conn():
    """
    Get a connection to the SQLite database.
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return AutoFKConnection(data_dir / "sqlite.db")
