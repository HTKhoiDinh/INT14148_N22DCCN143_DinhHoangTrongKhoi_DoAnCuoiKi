import re

from middleware.config_loader import load_security_policy


def normalize_sql(sql):
    if sql is None:
        return ""

    return " ".join(sql.strip().split())


def is_select_query(sql):
    normalized = normalize_sql(sql).upper()

    return normalized.startswith("SELECT")


def has_multiple_statements(sql):
    sql = sql.strip()

    if ";" not in sql:
        return False

    # Cho phép 1 dấu ; ở cuối câu SELECT
    if sql.endswith(";") and sql.count(";") == 1:
        return False

    return True


def contains_forbidden_keyword(sql, keywords):
    upper_sql = sql.upper()

    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword.upper()) + r"\b"

        if re.search(pattern, upper_sql):
            return keyword

    return None


def contains_forbidden_pattern(sql, patterns):
    upper_sql = sql.upper()

    for pattern in patterns:
        escaped_pattern = pattern.upper()

        # Một số pattern cần regex linh hoạt hơn
        if escaped_pattern == "OR 1=1":
            if re.search(r"\bOR\s+1\s*=\s*1\b", upper_sql):
                return pattern

        elif escaped_pattern == "OR TRUE":
            if re.search(r"\bOR\s+TRUE\b", upper_sql):
                return pattern

        elif escaped_pattern == "OR '1'='1'":
            if re.search(r"\bOR\s+'1'\s*=\s*'1'", upper_sql):
                return pattern

        elif escaped_pattern == "OR 'A'='A":
            if re.search(r"\bOR\s+'A'\s*=\s*'A'", upper_sql):
                return pattern

        else:
            if escaped_pattern in upper_sql:
                return pattern

    return None


def analyze_sql(sql):
    """
    Analyze SQL query based on config/security_policy.json.

    Return:
    {
        "allowed": True/False,
        "reason": "..."
    }
    """

    policy = load_security_policy()

    if sql is None or sql.strip() == "":
        return {
            "allowed": False,
            "reason": "EMPTY_QUERY"
        }

    normalized = normalize_sql(sql)

    if policy.get("only_select", True):
        if not is_select_query(normalized):
            return {
                "allowed": False,
                "reason": "ONLY_SELECT_ALLOWED"
            }

    if policy.get("block_multiple_statements", True):
        if has_multiple_statements(normalized):
            return {
                "allowed": False,
                "reason": "MULTIPLE_SQL_STATEMENTS"
            }

    keyword = contains_forbidden_keyword(
        normalized,
        policy.get("forbidden_keywords", [])
    )

    if keyword is not None:
        return {
            "allowed": False,
            "reason": f"FORBIDDEN_KEYWORD: {keyword}"
        }

    pattern = contains_forbidden_pattern(
        normalized,
        policy.get("forbidden_patterns", [])
    )

    if pattern is not None:
        return {
            "allowed": False,
            "reason": f"FORBIDDEN_PATTERN: {pattern}"
        }

    return {
        "allowed": True,
        "reason": "SAFE_QUERY"
    }


def detect(sql):
    """
    Compatibility function for evaluation.
    Return True if query should be blocked.
    """

    result = analyze_sql(sql)

    return not result["allowed"]