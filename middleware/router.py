def get_site(emp_id):
    """
    Horizontal fragmentation:
    Site 1: ID 1 -> 1000
    Site 2: ID 1001 -> 2000
    """

    if emp_id is None:
        return None

    if 1 <= emp_id <= 1000:
        return 1

    if 1001 <= emp_id <= 2000:
        return 2

    return None