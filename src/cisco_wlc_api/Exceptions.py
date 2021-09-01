"""
Exceptions used within cisco_wlc_api.
"""

# pylint: disable=invalid-name,import-error
from requests.packages.urllib3.exceptions import HTTPError


class WLCBaseException(HTTPError):
    """Base exception type used by cisco_wlc_api (this module)"""


class WLCAssertionException(WLCBaseException):
    """Base exception type used for internal assertions"""


class WLCSessionException(WLCBaseException):
    """Base exception type used for session-related errors"""


class WLCRequestException(WLCBaseException):
    """Base exception type used for request-related errors"""


class WLCFormatException(WLCBaseException):
    """Base exception type used for format-related errors"""


class WLCModelException(WLCBaseException):
    """Base exception type used for model-related errors"""


class IncorrectTypeError(WLCAssertionException):
    """Error raised when an argument is of an incorrect type"""


class IncorrectLengthError(WLCAssertionException):
    """Error raised when an argument has the wrong length"""


class UnexpectedResponseStatusError(WLCRequestException):
    """Error raised when a request returns an unexpected response code"""


class NotLoggedInError(WLCSessionException):
    """Error raised when a login attempt has yet to be made"""


class LoginFailureError(WLCSessionException):
    """Error raised when a login attempt fails"""


class SessionExpiredError(WLCSessionException):
    """Error raised when an established session's authentication has expired.
    Usually safe to retry."""


class ClientNotPresentError(WLCRequestException):
    """Error raised when a Client object refers to a non-existent client,
    or when a method that queries for a client returns no results"""


class QueryReturnedNoResultsError(WLCRequestException):
    """Error raised when a filtered query
    (eg. Endpoints.Clients.Client.RF(devicemacaddress=..)) returns no results"""


class NoPreviousRequestError(WLCRequestException):
    """Error raised when CiscoWLCAPISession.retry_last is called without there
    being a "last request" to retry."""


class NoPropertyError(WLCModelException):
    """Error raised when a method is called on a Model object when a required
    property is missing"""
