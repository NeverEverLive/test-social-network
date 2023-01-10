class PostException(Exception):
    def __init__(self, status_code: int = 400, message: str = "Post error"):
        self.status_code = status_code
        self.message = message


class PostNotExistException(PostException):
    pass

class PostPermissionException(PostException):
    pass