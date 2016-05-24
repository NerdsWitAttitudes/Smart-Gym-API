class NotUniqueException(Exception):
    """Exception if the data is not unique"""

    def __init__(self, message):
        self.message = message
