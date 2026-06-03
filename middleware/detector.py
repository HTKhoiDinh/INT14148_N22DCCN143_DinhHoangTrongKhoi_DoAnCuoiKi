import re


FORBIDDEN_PATTERNS = [
    r"\bDROP\b",
    r"\bTRUNCATE\b",
    r"\bUNION\b",
    r"--",
    r"/\*",
    r"\*/",
    r"\bDELETE\b",
    r"\bUPDATE\b",
    r"\bINSERT\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bEXEC\b",

    # Boolean-based SQL Injection
    r"\bOR\s+1\s*=\s*1\b",
    r"\bOR\s+TRUE\b",
    r"\bOR\s+'1'\s*=\s*'1'",
    r"\bOR\s+'a'\s*=\s*'a'",
    r"\bOR\s+'.+'\s*=\s*'.+'",
]


def normalize_sql(sql):
    return " ".join(sql.strip().split())


def is_select_query(sql):
    normalized = normalize_sql(sql).upper()
    return normalized.startswith("SELECT")


def has_multiple_statements(sql):
    """
    Cho phép dấu ; ở cuối câu.
    Chặn nếu có nhiều câu SQL nối tiếp nhau.
    """
    sql = sql.strip()

    if ";" not in sql:
        return False

    if sql.endswith(";") and sql.count(";") == 1:
        return False

    return True


def detect(sql):
    """
    Trả về True nếu phát hiện SQL nguy hiểm.
    Hàm này giữ lại để evaluate.py dùng.
    """
    result = analyze_sql(sql)
    return not result["allowed"]


def analyze_sql(sql):
    """
    Trả về thông tin chi tiết:
    {
        "allowed": True/False,
        "reason": "..."
    }
    """

    if sql is None or sql.strip() == "":
        return {
            "allowed": False,
            "reason": "EMPTY_QUERY"
        }

    normalized = normalize_sql(sql)
    upper_sql = normalized.upper()

    if not is_select_query(upper_sql):
        return {
            "allowed": False,
            "reason": "ONLY_SELECT_ALLOWED"
        }

    if has_multiple_statements(normalized):
        return {
            "allowed": False,
            "reason": "MULTIPLE_SQL_STATEMENTS"
        }

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, upper_sql, re.IGNORECASE):
            return {
                "allowed": False,
                "reason": f"FORBIDDEN_PATTERN: {pattern}"
            }

    return {
        "allowed": True,
        "reason": "SAFE_QUERY"
    }