from requests.packages.urllib3.exceptions import HTTPError


class WLCBaseException(HTTPError):
	"""Base exception type used by cisco_wlc_api (this module)"""

	pass


class WLCAssertionException(WLCBaseException):
	"""Base exception type used for internal assertions"""

	pass


class WLCSessionException(WLCBaseException):
	"""Base exception type used for session-related errors"""

	pass


class WLCRequestException(WLCBaseException):
	"""Base exception type used for request-related errors"""

	pass


class WLCFormatException(WLCBaseException):
	"""Base exception type used for format-related errors"""

	pass


class NotLoggedInError(WLCSessionException):
	"""Error raised when a login attempt has yet to be made"""

	pass


class LoginFailureError(WLCSessionException):
	"""Error raised when a login attempt fails"""

	pass


class SessionExpiredError(WLCSessionException):
	"""Error raised when an established session's authentication has expired. Usually safe to retry."""

	pass


class ClientNotPresentError(WLCRequestException):
	"""Error raised when a Client object refers to a non-existent client, or when a method that queries for a client returns no results"""

	pass


class NoPreviousRequestError(WLCRequestException):
	"""Error raised when CiscoWLCAPISession.retry_last is called without there being a "last request" to retry."""

	pass