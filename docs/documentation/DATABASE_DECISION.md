# Database Selection — Beta.ver.1.1 (LATEST)

**Status:** Dual-engine support is **fully integrated** in the codebase.

## Decision

The Hospital Management System uses a **configurable relational backend**:

| Mode | When to use | Configuration |
|------|-------------|----------------|
| **SQLite** | Zero-install, file-based demos, offline-friendly | `USE_MYSQL = False` in `src/config.py`; path in `SQLITE_CONFIG` |
| **MySQL** | XAMPP/lab or production-like setups | `USE_MYSQL = True` in `src/config.py`; credentials in `MYSQL_CONFIG` |

**No application code rewrites are required to switch engines** for normal operation: `src/database/__init__.py` selects **`MySQLDatabaseManager`** or the SQLite **`DatabaseManager`** and exposes a single **`DatabaseManager`** symbol to **`src/services/`** (strategy-style composition root). Services are written against that shared interface.

## Rationale

- **SQLite:** Built into Python, single file, easy backup and classroom use.
- **MySQL:** Familiar stack with **XAMPP**, closer to networked deployments, supports shared DB scenarios.
- **Same service layer:** Dependency injection keeps queue rules, appointment conflict logic, and reporting independent of the concrete engine.

## Schema and tooling

- Schema and initialization follow project scripts under `src/database/` and related SQL assets (see repository layout).
- Use **Navicat** or **phpMyAdmin** for MySQL; Navicat or file tools for SQLite as needed.

## Notes

- Parameter placeholders in SQL use `%s` style compatible with both managers where applicable.
- After changing `src/config.py`, **restart** the Streamlit app.

---

**Last updated:** March 2026 — aligned with Beta.ver.1.1 documentation.
