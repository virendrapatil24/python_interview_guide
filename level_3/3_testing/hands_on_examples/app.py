from typing import List, Dict

class Database:
    """Simulates a database connection"""
    def get_users(self) -> List[Dict]:
        # Imagine this connects to a real DB
        # In tests, we don't want to actually call this
        pass

    def save_user(self, user: Dict):
        # Writes to DB
        pass

class UserManager:
    def __init__(self, db: Database):
        self.db = db

    def get_user_names(self) -> List[str]:
        users = self.db.get_users()
        # Logic: Convert names to uppercase
        return [user['name'].upper() for user in users]

    def add_user(self, name: str) -> Dict:
        if not name:
            raise ValueError("Name cannot be empty")
        
        user = {"name": name, "active": True}
        self.db.save_user(user)
        return user

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
