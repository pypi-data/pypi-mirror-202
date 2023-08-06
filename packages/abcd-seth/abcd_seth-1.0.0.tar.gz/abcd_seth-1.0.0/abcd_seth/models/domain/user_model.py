import datetime


class User:
    def __init__(self, name: str, email: str, password: str, created_at: datetime):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
