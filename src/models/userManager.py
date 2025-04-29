import json
import os
from json import JSONDecodeError
from warnings import catch_warnings

from models.user import User

USER_DATA_FILE = 'users.json'
MAX_USERS = 3
START_BALANCE = 500


class UserManager:
    @staticmethod
    def load_users():
        if not os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'w') as f:
                f.write(json.dumps({}))

        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
                return {name: User(**info) for name, info in data.items()}
        except JSONDecodeError:
            with open(USER_DATA_FILE, 'w') as f:
                f.write(json.dumps({}))
            return UserManager.load_users()

    def __init__(self):
        self.users = self.load_users()

    def can_create_users(self):
        if len(self.users) < MAX_USERS: return True
        print("Maximum number of users reached")
        return False

    def save_users(self):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({u.nickname: u.to_dict() for u in self.users.values()}, f, indent=4)

    def get_user(self, nickname):
        return self.users.get(nickname)

    def register_user(self, nickname):
        if not self.can_create_users():
            return None
        user = User(nickname, START_BALANCE)
        self.users[nickname] = user
        print(f"Registered {nickname} with {START_BALANCE} coins")
        return user
