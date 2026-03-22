"""
Read seed_test_data_mysql.sql and write seed_test_data_sqlite.sql with SQLite syntax.

Run:
  python src/database/materialize_sqlite_seed.py
"""

import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MYSQL_PATH = os.path.join(HERE, "seed_test_data_mysql.sql")
SQLITE_PATH = os.path.join(HERE, "seed_test_data_sqlite.sql")

DEMO_HASH = hashlib.sha256(b"demo123").hexdigest()


def main():
    with open(MYSQL_PATH, "r", encoding="utf-8") as f:
        s = f.read()

    s = s.replace(
        "Hospital Management System — MySQL test / seed data",
        "Hospital Management System — SQLite test / seed data",
    )
    s = s.replace(
        "-- Prerequisites:\n"
        "--   1. CREATE DATABASE hospital_system CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\n"
        "--   2. USE hospital_system;\n"
        "--   3. Run schema_mysql.sql (creates empty tables + indexes).\n"
        "--   4. Run this script (loads reference + demo data).\n"
        "--\n"
        "-- Clears all application tables and reloads consistent rows. FK-safe order.\n"
        "-- Demo logins (users.password_hash = SHA2('demo123', 256)):\n"
        "--   admin / demo123   (Administrator)\n"
        "--   reception / demo123 (Receptionist)\n"
        "--\n"
        "-- SQLite: use seed_test_data_sqlite.sql after schema.sql (regenerate from this\n"
        "-- file with: python src/database/materialize_sqlite_seed.py).\n"
        "-- =============================================================================",
        "-- Prerequisites:\n"
        "--   1. Initialize with schema.sql (empty tables).\n"
        "--   2. Run this script (same logical data as MySQL seed).\n"
        "--\n"
        "-- Clears all application tables and reloads consistent rows. FK-safe order.\n"
        "-- Demo logins (password_hash = SHA-256 hex of demo123):\n"
        "--   admin / demo123   (Administrator)\n"
        "--   reception / demo123 (Receptionist)\n"
        "--\n"
        "-- Regenerate this file from seed_test_data_mysql.sql via materialize_sqlite_seed.py.\n"
        "-- =============================================================================",
    )
    s = re.sub(
        r"SET NAMES utf8mb4;\s*SET FOREIGN_KEY_CHECKS = 0;\s*"
        r"TRUNCATE TABLE audit_logs;\s*TRUNCATE TABLE queue_entries;\s*"
        r"TRUNCATE TABLE appointments;\s*TRUNCATE TABLE doctor_specializations;\s*"
        r"TRUNCATE TABLE doctors;\s*TRUNCATE TABLE patients;\s*"
        r"TRUNCATE TABLE users;\s*TRUNCATE TABLE specializations;\s*"
        r"SET FOREIGN_KEY_CHECKS = 1;",
        "PRAGMA foreign_keys = OFF;\n"
        "DELETE FROM audit_logs;\n"
        "DELETE FROM queue_entries;\n"
        "DELETE FROM appointments;\n"
        "DELETE FROM doctor_specializations;\n"
        "DELETE FROM doctors;\n"
        "DELETE FROM patients;\n"
        "DELETE FROM users;\n"
        "DELETE FROM specializations;\n"
        "PRAGMA foreign_keys = ON;",
        s,
        flags=re.DOTALL,
    )

    s = s.replace("SHA2('demo123', 256)", f"'{DEMO_HASH}'")

    # Datetime composites first (avoid partial substitution)
    s = re.sub(
        r"DATE_ADD\(DATE_SUB\(NOW\(\), INTERVAL (\d+) DAY\), INTERVAL (\d+) MINUTE\)",
        r"datetime('now', '-\1 day', '+\2 minute')",
        s,
    )

    s = re.sub(
        r"DATE_SUB\(NOW\(\), INTERVAL (\d+) HOUR\)",
        r"datetime('now', '-\1 hour')",
        s,
    )
    s = re.sub(
        r"DATE_SUB\(NOW\(\), INTERVAL (\d+) MINUTE\)",
        r"datetime('now', '-\1 minute')",
        s,
    )
    s = re.sub(
        r"DATE_SUB\(NOW\(\), INTERVAL (\d+) DAY\)",
        r"datetime('now', '-\1 day')",
        s,
    )

    s = re.sub(
        r"DATE_SUB\(CURDATE\(\), INTERVAL (\d+) DAY\)",
        r"date('now', '-\1 day')",
        s,
    )
    s = re.sub(
        r"DATE_ADD\(CURDATE\(\), INTERVAL (\d+) DAY\)",
        r"date('now', '+\1 day')",
        s,
    )
    s = re.sub(r"CURDATE\(\)", "date('now')", s)

    s = re.sub(
        r"\n-- Reset AUTO_INCREMENT to next free id \(optional safety after explicit ids\)\n"
        r"ALTER TABLE specializations AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE doctors AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE patients AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE appointments AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE queue_entries AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE users AUTO_INCREMENT = \d+;\n"
        r"ALTER TABLE audit_logs AUTO_INCREMENT = \d+;\n?",
        "\n-- SQLite: explicit PKs above update AUTOINCREMENT counters automatically.\n",
        s,
    )

    with open(SQLITE_PATH, "w", encoding="utf-8") as out:
        out.write(s)

    print(f"Wrote {SQLITE_PATH}")


if __name__ == "__main__":
    main()
