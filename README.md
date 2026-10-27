# vuln-demo

A small inventory tracker (Python CLI + C and C++ helpers) that is **deliberately insecure**.
It is made for testing static analysis tools (bandit, semgrep, cppcheck, flawfinder, clang-tidy, CodeQL).
Do not deploy it or copy its code into real projects.

```
app.py      CLI entry point
db.py       SQLite layer
auth.py     passwords, sessions, signatures
utils.py    reports, file access, small helpers
buffer.c    string helpers
cache.c     linked-list cache
parser.cpp  binary record parser
Makefile    builds the C/C++ demos (make)
```

## Answer key

### Real vulnerabilities (true positives)

| File | Where | Issue |
|---|---|---|
| db.py | `find_item` | SQL injection (`%` string formatting) |
| db.py | `find_user` | SQL injection (f-string) |
| app.py | `cmd_adjust` | Code injection via `eval` on user input |
| app.py | `cmd_import` | Insecure deserialization (`pickle.load` on a user file) |
| auth.py | `SECRET_KEY` | Hardcoded secret |
| auth.py | `hash_password` | MD5 used to hash passwords (no salt) |
| auth.py | `load_session` | Insecure deserialization (`pickle.loads` on a cookie) |
| utils.py | `run_report` | OS command injection (`os.system` with user input) |
| utils.py | `read_attachment` | Path traversal (`../` or absolute path escapes `BASE_DIR`) |
| buffer.c | `greet` | Stack buffer overflow (`strcpy` into 16 bytes) |
| buffer.c | `log_msg` | Format string bug (`printf(msg)`) |
| cache.c | `cache_evict` | Use after free (`e->key` read after `free(e)`) |
| cache.c | `cache_dump_leaky` | Memory leak (`strdup` never freed) |
| parser.cpp | `load_records` | Integer overflow in `count * record_size`, then heap overflow |
| parser.cpp | `copy_name` | Off-by-one heap overflow (`buf[len]` on a `len`-byte buffer) |

### False positives (flagged by pattern, not exploitable)

| File | Where | Typical tool warning | Why it is safe |
|---|---|---|---|
| db.py | `count_rows` | bandit B608 (SQL built from string) | Table name is checked against `ALLOWED_TABLES` |
| db.py | `list_items` | bandit B608 | Value is forced through `int()` and `%d` |
| auth.py | `PASSWORD_FIELD`, `RESET_URL`, `TOKEN_PLACEHOLDER` | bandit B105 (hardcoded password) | They are field names or URLs, not secrets |
| auth.py | `verify_signature` | "uses a secret key" or "HMAC" rules | Uses `hmac.compare_digest`, so the compare is constant-time |
| utils.py | `git_revision` | bandit B603 / B607 (subprocess, partial path) | Fixed argument list, no shell, no user input |
| utils.py | `cache_key` | bandit B324 (MD5) | Only a cache key, not a security use |
| utils.py | `retry_delay` | bandit B311 (`random`) | Retry jitter, not cryptography |
| utils.py | `sleep_quietly` | bandit B110 (try/except/pass) | Ignoring Ctrl-C during a sleep is intended |
| utils.py | `clamp_qty` | bandit B101 (assert) | The assert is a sanity check, and the value is clamped after it anyway |
| app.py | `check_status` | bandit B310 (urlopen) | URL is a hardcoded `https://` constant |
| buffer.c | `set_label` | flawfinder / cppcheck `strcpy` | Length is checked first |
| buffer.c | `print_id` | flawfinder `sprintf` | `n` is clamped to 0..9999, so the output is at most 7 bytes |
| buffer.c | `copy_tag` | `strncpy` warnings | NUL terminator is set by hand |
| cache.c | `cache_shutdown` | double free | Second `free(NULL)` is a no-op |
| cache.c | `show_first` | use after free (`line` used after `free`) | `line` is set to NULL, so the second `if` never runs |
| cache.c | `format_entry` | `malloc` + `snprintf` | Size is computed, result is checked and bounded |
| parser.cpp | `read_header` | `memcpy` | Size is checked first |
| parser.cpp | `field_at` | `vector::operator[]` | Index is bounds-checked first |
| parser.cpp | `set_unit` | `strncpy` | Terminated by hand, size comes from the array type |

## Try it

```
pip install bandit && bandit -r .
cppcheck --enable=all buffer.c cache.c parser.cpp
flawfinder .
make            # builds ./buffer ./cache ./parser
```
