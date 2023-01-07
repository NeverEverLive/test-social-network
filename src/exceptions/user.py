class UserException(Exception):
    def __init__(self, status_code: int = 400, message: str = "User Error"):
        self.status_code = status_code
        self.message = message


class UserNotExist(UserException):
    pass