"""Misc helpers: reports, file access, small conveniences."""
import hashlib
import os
import random
import subprocess
import time

BASE_DIR = os.path.abspath("data")


def run_report(item_name):
    os.system("grep -i %s data/items.txt | sort" % item_name)


def read_attachment(filename):
    with open(os.path.join(BASE_DIR, filename), "rb") as fh:
        return fh.read()


def git_revision():
    out = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return out.stdout.strip()


def cache_key(*parts):
    joined = "|".join(str(p) for p in parts)
    return hashlib.md5(joined.encode()).hexdigest()


def retry_delay(attempt):
    return min(30, 2 ** attempt) + random.uniform(0, 0.5)


def sleep_quietly(seconds):
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass


def clamp_qty(qty):
    assert isinstance(qty, int), "qty must be an int"
    return max(0, min(qty, 10_000))
