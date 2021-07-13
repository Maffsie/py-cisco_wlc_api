from .Exceptions import WLCAssertionException
from .Decorators import validator
import re


class Patterns:
    """Patterns for regular expression matching; mostly pulled from the WLC Angular app source"""
    MAC = re.compile(r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')


def _assert(condition: bool, message: str) -> bool:
    if not condition:
        raise WLCAssertionException(message)


@validator
def simple(
        condition: bool = False,
        message_on_failure: str = "",
        message_for_remediation: str = "",
        exception_type: BaseException = WLCAssertionException
) -> bool:
    if not condition:
        raise exception_type(
            message=message_on_failure,
            msg_remedial=message_for_remediation
        )


@validator
def baseurl(url: str):
    _assert(re.match("^https?://", url), f"Base URL parameter ('{url}') must begin with http(s)://")
    _assert(not url.endswith("/"), f"Base URL parameter ('{url}') must not end with a forward-slash")


@validator
def length(item, size):
    _assert(len(item) == size,
            f"Object expected to be of size {size}, but was actually {len(item)}")


@validator
def credential(credentials: tuple):
    _assert(type(credentials) is tuple,
            f"Credentials parameter must be a tuple, but given object was actually a {type(credentials)}")
    _assert(len(credentials) == 2,
            f"Credentials parameter must contain a username and a password, but given object contained {len(credentials)} item(s)")


@validator
def status_firstlogin(code):
    _assert(code in (200, 401),
            f"Stage 1 of login process should have returned HTTP 200 or 401, but actually returned {code}.")

@validator
def status(code):
    _assert(code == 200,
            f"HTTP request should have returned HTTP 200, but actually returned {code}")
