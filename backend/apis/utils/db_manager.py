"""

    DB CONNECTION MANAGER UTILITY.
    Utilities for managing connections to db.

"""
from sqlite3 import connect

from .path_manager import db_paths as paths


def connection_preset(db_con):
    """
    Preset the connection by disabling rollback journal, setting the locking mode to exclusive,
    disabling sync and setting up the directory for temporary files.
    Args:
        db_con: The database connection to preset

    """
    db_con.execute("pragma journal_mode=OFF;")  # disables the rollback journal completely
    db_con.execute("pragma locking_mode=EXCLUSIVE;")  # never releases file-locks
    db_con.execute("pragma synchronous=OFF;")  # continues without syncing
    db_con.execute(f"pragma temp_store_directory='{paths.temp_dir}';")  # temporary tables and indices folder


def clear_db(db_name=None, db_con=None, db_cur=None):
    """
    Clear the given database (specifying either its name or the connection and the cursor)
    by removing all tables, indexes and triggers
    Args:
        db_name:    The path to the database file
        db_con:     An already existing connection to the database, if owned
        db_cur:     An already existing cursor for the database, if owned


    """
    if db_con is None or db_cur is None:
        close_flag = True
        db_con = connect(db_name)
        connection_preset(db_con)
        db_cur = db_con.cursor()
    else:
        close_flag = False

    db_con.execute("pragma writable_schema=1;")
    db_cur.execute("DELETE FROM sqlite_master WHERE type in ('table', 'index', 'trigger')")
    db_con.execute("pragma writable_schema=0;")
    db_con.commit()
    db_con.execute("vacuum")
    if close_flag:
        db_con.close()
