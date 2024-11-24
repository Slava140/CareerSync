from uuid import UUID


class InvalidEmailOrPasswordError(Exception):
    def __init__(self):
        super().__init__(f"Invalid email or password")


class UserWithUUIDAlreadyHasMaximumRefreshSessionsError(Exception):
    def __init__(self, uuid: UUID, count: int):
        super().__init__(f"User(uuid={uuid}) already has {count} active sessions")


class RefreshSessionNotFoundError(Exception):
    def __init__(self):
        super().__init__("Refresh session was not found")


class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__("Token is invalid")


class UserAlreadyExistsError(Exception):
    def __init__(self, what_exists: str = '', value=''):
        user_part = 'User'
        if what_exists.strip() and value.strip():
            user_part = f"User({what_exists}=\"{str(value)}\")"

        super().__init__(f"{user_part} already exists")


class UserNotFoundError(Exception):
    def __init__(self, what_not_found: str = '', value=''):
        user_part = 'User'
        if what_not_found.strip() and value.strip():
            user_part = f"User({what_not_found}=\"{str(value)}\")"

        super().__init__(f"{user_part} was not found")

