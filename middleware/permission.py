from middleware.config_loader import load_user_policy


def allowed(user, fragment):
    """
    Check whether a user can access a distributed fragment.

    user: alice, bob, charlie, auditor, admin
    fragment: dictionary from fragment_config.json
    """

    if user is None or fragment is None:
        return False

    user = user.strip().lower()

    user_policy = load_user_policy()

    if user not in user_policy:
        return False

    allowed_sites = user_policy[user]

    return fragment["site"] in allowed_sites


def get_user_sites(user):
    if user is None:
        return []

    user = user.strip().lower()

    user_policy = load_user_policy()

    return user_policy.get(user, [])