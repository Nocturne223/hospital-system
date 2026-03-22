"""
Load MySQL test/seed data for the Hospital Management System.

Runs src/database/seed_test_data_mysql.sql using MYSQL_CONFIG from src/config.py.
This TRUNCATES application tables then inserts the full demo dataset.

Usage (from project root):
    python seed_mysql_data.py          # prompts for confirmation
    python seed_mysql_data.py --yes    # non-interactive (CI / scripts)

Requires: pip install mysql-connector-python
"""

from __future__ import annotations

import argparse
import os
import re
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

try:
    import mysql.connector
    from mysql.connector import errors as mysql_errors
except ImportError:
    print("ERROR: mysql-connector-python is not installed.")
    print("Install with: python -m pip install mysql-connector-python")
    sys.exit(1)

try:
    from config import MYSQL_CONFIG
except ImportError:
    print("ERROR: Could not import MYSQL_CONFIG from src/config.py")
    sys.exit(1)

from database.mysql_sql_split import split_mysql_statements

SEED_PATH = os.path.join(_ROOT, "src", "database", "seed_test_data_mysql.sql")

EXPECTED_TABLES = [
    "patients",
    "doctors",
    "specializations",
    "doctor_specializations",
    "queue_entries",
    "appointments",
    "users",
    "audit_logs",
]


def _non_comment_body(stmt: str) -> str:
    return "\n".join(
        line for line in stmt.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ).strip()


def apply_seed() -> int:
    if not os.path.isfile(SEED_PATH):
        raise FileNotFoundError(f"Seed file not found: {SEED_PATH}")

    with open(SEED_PATH, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)

    cfg = {**MYSQL_CONFIG, "connection_timeout": 10, "autocommit": False}
    conn = mysql.connector.connect(**cfg)
    cursor = None
    try:
        cursor = conn.cursor()
        statements = split_mysql_statements(raw)
        ran = 0
        for stmt in statements:
            if not _non_comment_body(stmt):
                continue
            try:
                cursor.execute(stmt)
                ran += 1
            except mysql_errors.Error as e:
                raise RuntimeError(
                    f"MySQL error on statement:\n{stmt[:280]}...\n\n{e}"
                ) from e
        conn.commit()
        print(f"Seed complete: {ran} statement(s) executed ({SEED_PATH})")
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    cfg_ro = {**MYSQL_CONFIG, "connection_timeout": 10, "autocommit": True}
    conn = mysql.connector.connect(**cfg_ro)
    try:
        cur = conn.cursor()
        print("\nRow counts:")
        for table in EXPECTED_TABLES:
            cur.execute(f"SELECT COUNT(*) FROM `{table}`")
            n = cur.fetchone()[0]
            print(f"  {table}: {n}")
        cur.close()
    finally:
        conn.close()

    return ran


def main() -> int:
    parser = argparse.ArgumentParser(description="Load MySQL seed data (truncates tables).")
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Do not prompt; use when you accept wiping existing rows in these tables.",
    )
    args = parser.parse_args()

    print("Hospital Management System - MySQL seed data")
    print(f"  Host: {MYSQL_CONFIG.get('host')}:{MYSQL_CONFIG.get('port')}")
    print(f"  Database: {MYSQL_CONFIG.get('database')}")
    print(f"  User: {MYSQL_CONFIG.get('user')}")
    print()
    print("WARNING: The seed script TRUNCATES all application tables, then reloads demo rows.")

    if not args.yes:
        try:
            answer = input("Continue? [y/N]: ").strip().lower()
        except EOFError:
            answer = ""
        if answer != "y":
            print("Cancelled.")
            return 0

    try:
        apply_seed()
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    print("\nDemo users (password: demo123): admin, reception, nurse.mina, dr.ruiz, viewer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
