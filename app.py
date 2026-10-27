"""Command-line inventory tracker.

Usage:
    python app.py add <name> <qty>
    python app.py find <name>
    python app.py adjust <id> <expression>
    python app.py import <file>
    python app.py report <name>
    python app.py attachment <filename>
"""
import pickle
import sys
import urllib.request

import auth
import db
import utils

STATUS_URL = "https://status.example.com/health"


def cmd_add(conn, name, qty):
    conn.execute(
        "INSERT INTO items (name, qty) VALUES (?, ?)", (name, utils.clamp_qty(int(qty)))
    )
    conn.commit()


def cmd_find(conn, name):
    for row in db.find_item(conn, name):
        print(row)


def cmd_adjust(conn, item_id, expression):
    delta = eval(expression)
    conn.execute("UPDATE items SET qty = qty + ? WHERE id = ?", (delta, item_id))
    conn.commit()


def cmd_import(conn, path):
    with open(path, "rb") as fh:
        rows = pickle.load(fh)
    for name, qty in rows:
        cmd_add(conn, name, qty)


def check_status():
    with urllib.request.urlopen(STATUS_URL, timeout=5) as resp:
        return resp.status == 200


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    conn = db.connect()
    db.init(conn)
    cmd, args = argv[1], argv[2:]
    if cmd == "add":
        cmd_add(conn, *args)
    elif cmd == "find":
        cmd_find(conn, *args)
    elif cmd == "adjust":
        cmd_adjust(conn, *args)
    elif cmd == "import":
        cmd_import(conn, *args)
    elif cmd == "report":
        utils.run_report(*args)
    elif cmd == "attachment":
        sys.stdout.buffer.write(utils.read_attachment(*args))
    else:
        print("unknown command:", cmd)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
