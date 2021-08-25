from .Exceptions import LoginFailureError


def must_auth(function):
    def wrapper(self, *args, **kwargs):
        if self.authenticated:
            return function(self, *args, **kwargs)
        self.login()
        if not self.authenticated:
            raise LoginFailureError("Unable to call authenticated function: automatic logon failed")
        return function(self, *args, **kwargs)
    return wrapper


def validator(function):
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        return True
    return wrapper
