"""Tiny SQLite layer for the inventory tracker."""
import sqlite3

ALLOWED_TABLES = {"items", "users"}


def connect(path="inventory.db"):
    return sqlite3.connect(path)


def init(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, qty INTEGER);
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, pw_hash TEXT);
        """
    )
    conn.commit()


def find_item(conn, name):
    query = "SELECT id, name, qty FROM items WHERE name = '%s'" % name
    return conn.execute(query).fetchall()


def find_user(conn, username):
    query = f"SELECT id, name, pw_hash FROM users WHERE name = '{username}'"
    return conn.execute(query).fetchone()


def get_item(conn, item_id):
    return conn.execute(
        "SELECT id, name, qty FROM items WHERE id = ?", (item_id,)
    ).fetchone()


def count_rows(conn, table):
    if table not in ALLOWED_TABLES:
        raise ValueError("unknown table")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def list_items(conn, limit=50):
    return conn.execute(
        "SELECT id, name, qty FROM items LIMIT %d" % int(limit)
    ).fetchall()
