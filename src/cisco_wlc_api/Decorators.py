# pylint: disable=invalid-name

"""
Decorators for methods in the cisco_wlc_api module
"""

from .Exceptions import LoginFailureError


def must_auth(function):
    """Decorator to ensure that a function is only called if the session
    is authenticated"""

    def wrapper(self, *args, **kwargs):
        if self.authenticated:
            return function(self, *args, **kwargs)
        self.login()
        if not self.authenticated:
            raise LoginFailureError(
                "Unable to call authenticated function: automatic logon failed"
            )
        return function(self, *args, **kwargs)

    return wrapper


def validator(function):
    """Simple decorator used by validation functions that will
    normally only return a value if a condition is not met"""

    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        return True

    return wrapper
