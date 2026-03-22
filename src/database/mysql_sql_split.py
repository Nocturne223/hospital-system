"""
Split a MySQL script into statements on semicolons outside of quotes.
Handles ';' inside string literals and inside '--' line comments.
"""


def _strip_line_comments(sql: str) -> str:
    """Remove `-- ...` line comments when not inside single/double-quoted strings."""
    out: list[str] = []
    i = 0
    n = len(sql)
    in_single = False
    in_double = False
    escape = False

    while i < n:
        ch = sql[i]
        if escape:
            out.append(ch)
            escape = False
            i += 1
            continue
        if ch == "\\" and (in_single or in_double):
            out.append(ch)
            escape = True
            i += 1
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            i += 1
            continue
        if not in_single and not in_double and ch == "-" and i + 1 < n and sql[i + 1] == "-":
            i += 2
            while i < n and sql[i] not in "\n\r":
                i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def split_mysql_statements(sql: str) -> list[str]:
    sql = _strip_line_comments(sql)
    statements: list[str] = []
    current: list[str] = []
    in_single = False
    in_double = False
    escape = False

    for ch in sql:
        if escape:
            current.append(ch)
            escape = False
            continue
        if ch == "\\" and (in_single or in_double):
            current.append(ch)
            escape = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            current.append(ch)
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            current.append(ch)
            continue
        if ch == ";" and not in_single and not in_double:
            stmt = "".join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
            continue
        current.append(ch)

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements
