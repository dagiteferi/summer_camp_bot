import json
from src.constants import ADMIN_FILE

class AdminService:
    def __init__(self):
        self._admins = set()

    def load_admins(self):
        """Load admin user IDs from the JSON file."""
        try:
            with open(ADMIN_FILE, "r") as f:
                data = json.load(f)
                self._admins = set(data.get("admins", []))
        except FileNotFoundError:
            self._admins = set() # No admins yet

    def _save_admins(self):
        """Save the current list of admin IDs to the JSON file."""
        with open(ADMIN_FILE, "w") as f:
            json.dump({"admins": list(self._admins)}, f, indent=2)

    def is_admin(self, user_id):
        """Check if a user is an admin."""
        return user_id in self._admins

    def add_admin(self, user_id):
        """Add a new admin and save the updated list."""
        if user_id not in self._admins:
            self._admins.add(user_id)
            self._save_admins()
            return True
        return False

    def remove_admin(self, user_id):
        """Remove an admin from the list."""
        if user_id in self._admins:
            self._admins.remove(user_id)
            self._save_admins()
            return True
        return False

    def get_admins(self):
        """Get the current list of admin IDs."""
        return list(self._admins)