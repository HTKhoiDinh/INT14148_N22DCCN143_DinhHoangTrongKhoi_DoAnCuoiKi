import re


def extract_id(sql):
    """
    Trích xuất Employee ID từ câu SQL.

    Hỗ trợ:
    SELECT * FROM Employee WHERE ID=100
    SELECT * FROM Employee WHERE ID = 100
    select * from Employee where id=100
    """

    if sql is None:
        return None

    match = re.search(
        r"\bID\s*=\s*(\d+)\b",
        sql,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None