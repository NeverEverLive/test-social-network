class AuthenticationException(Exception):
    def __init__(self, status_code: int = 400, message: str = "Incorrect Token"):
        self.status_code = status_code
        self.message = message



class TokenExpiredException(AuthenticationException):
    pass


class InvalidTokenException(AuthenticationException):
    pass
