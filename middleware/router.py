from middleware.config_loader import load_fragment_config


def get_fragment(table_name, key_value):
    """
    Find the distributed fragment that contains the requested key value.

    Example:
    table_name = "Employee"
    key_value = 1500
    => site2
    """

    fragment_config = load_fragment_config()

    if table_name not in fragment_config:
        return None

    fragments = fragment_config[table_name]

    for fragment in fragments:
        min_value = fragment["min"]
        max_value = fragment["max"]

        if min_value <= key_value <= max_value:
            return fragment

    return None


def get_site(emp_id):
    """
    Backward-compatible function for old code.
    Returns only site_id.
    """

    fragment = get_fragment("Employee", emp_id)

    if fragment is None:
        return None

    return fragment["site_id"]


def get_db_path(table_name, key_value):
    """
    Return db_path based on fragment metadata.
    """

    fragment = get_fragment(table_name, key_value)

    if fragment is None:
        return None

    return fragment["db_path"]