permissions = {
    "alice": [1],
    "bob": [2],
    "admin": [1, 2]
}


def allowed(user, site):
    if user is None:
        return False

    user = user.strip().lower()

    if user not in permissions:
        return False

    return site in permissions[user]


def get_user_sites(user):
    if user is None:
        return []

    user = user.strip().lower()

    return permissions.get(user, [])