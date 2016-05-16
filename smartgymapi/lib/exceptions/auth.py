class UserFoundException(Exception):
    """Exception if the new user already exists."""

    def __init__(self, message):
        self.message = message
