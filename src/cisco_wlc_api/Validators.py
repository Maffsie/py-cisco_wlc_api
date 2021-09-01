# pylint: disable=invalid-name

"""
Validation class, providing module-level assertions that aren't "real" assertions
"""

import re

from requests import Response

from .Decorators import validator
from .Exceptions import (
    IncorrectLengthError,
    IncorrectTypeError,
    UnexpectedResponseStatusError,
    WLCAssertionException,
)


# pylint: disable=too-few-public-methods
class Patterns:
    """Patterns for regular expression matching; partly from the WLC Angular app source"""

    URLPROTO = re.compile(r"^https?://")
    MAC = re.compile(r"^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$")


def _assert(
    condition: bool, message: str, exception_type: BaseException = WLCAssertionException
) -> bool:
    if not condition:
        raise exception_type(message)


def _is_type(in_obj, expect_type: type, message: str = None) -> bool:
    _assert(
        isinstance(expect_type, type),
        "Nested assertions? they do happen." "expect_type param must be a type.",
    )
    _assert(
        isinstance(in_obj, expect_type),
        exception_type=IncorrectTypeError,
        message=message
        if message is not None
        else f"Expected an object of type {expect_type}, but input object"
        f" was of type {type(in_obj)}",
    )


@validator
def simple(
    condition: bool = False,
    message_on_failure: str = "",
    message_for_remediation: str = "",
    exception_type: BaseException = WLCAssertionException,
) -> bool:
    """Simple validator to check that a condition is true,
    raises an exception with message and remediation information if not"""
    if not condition:
        raise exception_type(
            message=message_on_failure, msg_remedial=message_for_remediation
        )


@validator
def baseurl(url: str):
    """Validate that the base_uri parameter is conformant"""
    _is_type(
        url,
        str,
        f"Base URL parameter should be a string, but was actually of type {type(url)}",
    )
    _assert(
        Patterns.URLPROTO.match(url),
        f"Base URL parameter ('{url}') must begin with http(s)://",
    )
    _assert(
        not url.endswith("/"),
        f"Base URL parameter ('{url}') must not end with a forward-slash",
    )


@validator
def length(item, size: int, message: str = None):
    """Validate that the length of an object is what is expected"""
    _assert(
        len(item) == size,
        exception_type=IncorrectLengthError,
        message=message
        if message is not None
        else f"Object expected to be of size {size}, but was actually {len(item)}",
    )


@validator
def credential(credentials: tuple):
    """Validate that a credentials parameter is correct"""
    _is_type(
        credentials,
        tuple,
        "Credentials parameter must be a tuple, but "
        f"given object was actually {type(credentials)}",
    )
    length(
        credentials,
        size=2,
        message=(
            "Credentials parameter must contain "
            "a username and a password, but given "
            f"object contained {len(credentials)} item(s)"
        ),
    )
    _is_type(
        credentials[0],
        str,
        f"Username must be a string, but was actually {type(credentials[0])}",
    )
    _is_type(
        credentials[1],
        str,
        f"Password must be a string, but was actually {type(credentials[1])}",
    )


@validator
def response_code(response: Response, expect: tuple[int] = (200,)):
    """Validate the response code of a requests Response object"""
    _is_type(
        response,
        expect_type=Response,
        message="Expected a Response object, but"
        f"got an object of type {type(response)} instead.",
    )
    _is_type(
        expect,
        expect_type=tuple,
        message="Expected a tuple of expected response codes, but got an "
        f"object of type {type(expect)} instead.",
    )
    for single_expected_code in expect:
        _is_type(
            single_expected_code,
            expect_type=int,
            message="Expected a tuple of expected response code integers, "
            f"but one or more was of type {type(single_expected_code)} instead.",
        )
    _assert(
        response.status_code in expect,
        exception_type=UnexpectedResponseStatusError,
        message=f"{response.request.method} '{response.url}' returned status "
        f"{response.status_code}, expected one of {expect}",
    )
