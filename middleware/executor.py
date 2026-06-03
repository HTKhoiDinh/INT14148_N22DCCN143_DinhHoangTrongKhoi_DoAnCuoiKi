import sqlite3


def execute_query(fragment, emp_id):
    """
    Execute a safe parameterized query on the selected distributed fragment.

    The middleware does NOT execute the raw SQL from the user.
    It only uses:
    - db_path from fragment_config.json
    - emp_id extracted by parser
    """

    if fragment is None:
        return None

    db_path = fragment["db_path"]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ID,
            Name,
            Department,
            Region,
            Salary,
            TaxCode,
            HealthStatus,
            BankAccount
        FROM Employee
        WHERE ID = ?
        """,
        (emp_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result