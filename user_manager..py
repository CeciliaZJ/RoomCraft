import json
import hashlib
import getpass # Although not used for API, we keep it for potential CLI use
import os

##This project was developed with the assistance of ChatGPT on 10/04/2025.

class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.users = self._load_users()

    def _load_users(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {} # Return empty dict if file is empty or corrupted
        return {}

    def _save_users(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=4)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # --- NEW API-FRIENDLY REGISTER METHOD ---
    def register_api(self, username, password):
        """Handles user registration for the API."""
        username = username.lower()
        if not (4 <= len(username) <= 20):
            return {"success": False, "message": "Username must be between 4 and 20 characters."}
        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters long."}
        if username in self.users:
            return {"success": False, "message": "Username already exists. Please choose another."}

        self.users[username] = self._hash_password(password)
        self._save_users()
        return {"success": True, "message": "Registration successful! You can now log in."}

    def login_api(self, username, password):
        """API-friendly login. Takes data as arguments, returns username or None."""
        if not username or not password:
            return None

        hashed_password = self._hash_password(password)
        if self.users.get(username.lower()) == hashed_password:
            return username.lower()
        else:
            return None
