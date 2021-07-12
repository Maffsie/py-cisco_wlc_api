def authenticate(function):
    def wrapper(self, *args, **kwargs):
        if self.authenticated: return function(self, *args, **kwargs)
        self.login()
        assert self.authenticated, "Unable to call authenticated function: automatic logon failed"
        return function(self, *args, **kwargs)
    return wrapper

def validator(function):
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        return True
    return wrapper
