class AuthorizationHeaderNotFound(Exception):
    """Exception raised when no authorization header is found"""

    def __init__(self):
        self.message = "No authorization header found"


class InvalidAuthorizationMethod(Exception):
    """
    Exception raised when the authorization method
    is not what was expected
    """

    def __init__(self, auth_method):
        self.message = "Wrong authorization method, expected method: {}"\
                .format(auth_method)
