import json

ADMIN_FILE = "config/admins.json"

def get_admins():
    """Reads the list of admin IDs from the JSON file."""
    try:
        with open(ADMIN_FILE, "r") as f:
            data = json.load(f)
            return data.get("admins", [])
    except FileNotFoundError:
        return []

def is_admin(user_id):
    """Checks if a user is an admin."""
    return user_id in get_admins()

def add_admin(user_id):
    """Adds a new admin to the list."""
    admins = get_admins()
    if user_id not in admins:
        admins.append(user_id)
        with open(ADMIN_FILE, "w") as f:
            json.dump({"admins": admins}, f, indent=2)
        return True
    return False

def remove_admin(user_id):
    """Removes an admin from the list."""
    admins = get_admins()
    if user_id in admins:
        admins.remove(user_id)
        with open(ADMIN_FILE, "w") as f:
            json.dump({"admins": admins}, f, indent=2)
        return True
    return False
