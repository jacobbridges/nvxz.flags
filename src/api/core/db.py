import aiosqlite


def get_conn():
    """
    Get a connection to the SQLite database.
    """
    return aiosqlite.connect("sqlite.db")
