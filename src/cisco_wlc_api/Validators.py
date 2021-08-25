from .Exceptions import WLCAssertionException
from .Decorators import validator
import re


class Patterns:
    """Patterns for regular expression matching; mostly pulled from the WLC Angular app source"""
    URLPROTO = re.compile(r'^https?://')
    MAC = re.compile(r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')


def _assert(condition: bool, message: str) -> bool:
    if not condition:
        raise WLCAssertionException(message)


def _is_type(in_obj, expect_type: type, message: str = None) -> bool:
    _assert(type(expect_type) is type, "Nested assertions? they do happen. expect_type param must be a type.")
    _assert(type(in_obj) is expect_type, message if message is not None else
            f"Expected an object of type {expect_type}, but input object was of type {type(in_obj)}")


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
    _is_type(url, str, f"Base URL parameter should be a string, but was actually of type {type(url)}")
    _assert(Patterns.URLPROTO.match(url), f"Base URL parameter ('{url}') must begin with http(s)://")
    _assert(not url.endswith("/"), f"Base URL parameter ('{url}') must not end with a forward-slash")


@validator
def length(item, size: int, message: str = None):
    _assert(len(item) == size, message if message is not None else
            f"Object expected to be of size {size}, but was actually {len(item)}")


@validator
def credential(credentials: tuple):
    _is_type(credentials, tuple,
             f"Credentials parameter must be a tuple, but given object was actually {type(credentials)}")
    _assert(len(credentials) == 2,
            f"Credentials parameter must contain a username and a password, but given object contained {len(credentials)} item(s)")
    _is_type(credentials[0], str,
             f"Username must be a string, but was actually {type(credentials[0])}")
    _is_type(credentials[1], str,
             f"Password must be a string, but was actually {type(credentials[1])}")


@validator
def response_code(response, expect=(200,)):
    _assert(response.status_code in expect,
            f"{response.request.method} '{response.url}' returned status {response.status_code}, "
            f"expected one of {expect}")
