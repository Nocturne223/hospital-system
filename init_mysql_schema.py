"""
Create MySQL tables for the Hospital Management System.

Uses src/config.py (MYSQL_CONFIG). Ensures the database exists, then runs
src/database/schema_mysql.sql.

Usage (from project root):
    python init_mysql_schema.py

Requires: pip install mysql-connector-python
"""

from __future__ import annotations

import os
import re
import sys

# Project root -> add src for config
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

SCHEMA_PATH = os.path.join(_ROOT, "src", "database", "schema_mysql.sql")


def _ensure_database_exists() -> None:
    db_name = MYSQL_CONFIG.get("database")
    if not db_name:
        raise ValueError("MYSQL_CONFIG['database'] is not set")

    server_cfg = {k: v for k, v in MYSQL_CONFIG.items() if k != "database"}
    server_cfg.setdefault("connection_timeout", 10)
    server_cfg.setdefault("autocommit", True)

    conn = mysql.connector.connect(**server_cfg)
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
        )
        cursor.close()
    finally:
        conn.close()


def apply_schema() -> None:
    if not os.path.isfile(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        raw = f.read()

    # Drop block comments /* ... */ (schema has none, but safe)
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)

    _ensure_database_exists()

    cfg = {**MYSQL_CONFIG, "connection_timeout": 10, "autocommit": False}
    conn = mysql.connector.connect(**cfg)
    cursor = None
    try:
        cursor = conn.cursor()
        statements = split_mysql_statements(raw)
        ran = 0
        for stmt in statements:
            # Skip pure comments / empty
            stripped = "\n".join(
                line for line in stmt.splitlines()
                if line.strip() and not line.strip().startswith("--")
            ).strip()
            if not stripped:
                continue
            try:
                cursor.execute(stmt)
                ran += 1
            except mysql_errors.Error as e:
                # 1050 = table exists, 1061 = duplicate key name — idempotent re-runs
                if e.errno in (1050, 1061):
                    continue
                raise RuntimeError(f"MySQL error on statement:\n{stmt[:200]}...\n\n{e}") from e
        conn.commit()
        print(f"Applied schema: {ran} statement(s) executed ({SCHEMA_PATH})")
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def main() -> int:
    print("Hospital Management System - MySQL schema")
    print(f"  Host: {MYSQL_CONFIG.get('host')}:{MYSQL_CONFIG.get('port')}")
    print(f"  Database: {MYSQL_CONFIG.get('database')}")
    print(f"  User: {MYSQL_CONFIG.get('user')}")
    print()

    try:
        apply_schema()
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    cfg = {**MYSQL_CONFIG, "connection_timeout": 10, "autocommit": True}
    conn = mysql.connector.connect(**cfg)
    try:
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]
        cur.close()
        print(f"Tables in `{MYSQL_CONFIG['database']}`: {', '.join(sorted(tables))}")
    finally:
        conn.close()

    print("\nOptional: load test data:")
    print("  python seed_mysql_data.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
