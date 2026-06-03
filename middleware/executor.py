import sqlite3


def get_database_path(site):
    if site == 1:
        return "database/site1.db"

    if site == 2:
        return "database/site2.db"

    return None


def execute_query(site, emp_id):
    """
    Không chạy raw SQL trực tiếp.
    Chỉ chạy parameterized query để tránh SQL Injection.
    """

    db_path = get_database_path(site)

    if db_path is None:
        return None

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT ID, Name, Department FROM Employee WHERE ID = ?",
        (emp_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result