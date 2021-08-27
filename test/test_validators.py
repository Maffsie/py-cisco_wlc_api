"""
Tests for the validation functionality in this module
"""

import pytest
from requests import Request, Response
# pylint: disable=import-error
import src.cisco_wlc_api.Validators as CiscoWLCAPIValidators
import src.cisco_wlc_api.Exceptions as CiscoWLCAPIExceptions


# Test data
length_test_a = [
    'one',
    'two',
    'three',
    'four',
]
length_test_b = (
    'one',
    'two',
    'three',
    'four',
    'five',
)
length_test_c = (
    'one',
    ('one', 'two',),
    ('two',),
    'three',
)
response_test_a = Response()
response_test_a.status_code = 200
response_test_a.request = Request()
response_test_a.request.method = 'put'
response_test_a.request.url = 'http://test-url'
response_test_b = Response()
response_test_b.status_code = 401
response_test_b.request = Request()
response_test_b.request.method = 'get'
response_test_b.request.url = 'http://test-url'
response_test_c = Response()
response_test_c.status_code = 503
response_test_c.request = Request()
response_test_c.request.method = 'post'
response_test_c.request.url = 'http://test-url'


def test_baseurl_type_enforcement():
    """Test that an incorrect type URL parameter correctly
    raises an exception"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.baseurl(url=int(42))


def test_baseurl_urlproto_match():
    """Test that an invalid or missing protocol correctly raises
    an exception"""
    with pytest.raises(CiscoWLCAPIExceptions.WLCAssertionException):
        CiscoWLCAPIValidators.baseurl(url='127.0.0.1')
    with pytest.raises(CiscoWLCAPIExceptions.WLCAssertionException):
        CiscoWLCAPIValidators.baseurl(url='hxxp://127.0.0.1')


def test_baseurl_suffix():
    """Test that a base URL with a trailing slash correctly fails validation"""
    with pytest.raises(CiscoWLCAPIExceptions.WLCAssertionException):
        CiscoWLCAPIValidators.baseurl(url='http://127.0.0.1/')


def test_baseurl_succeeds():
    """Test that valid base URLs are correctly validated"""
    assert CiscoWLCAPIValidators.baseurl(url='http://127.0.0.1')
    assert CiscoWLCAPIValidators.baseurl(url='https://cisco-wlc-web-ui.local')


def test_length_wrong():
    """Test that an IncorrectLengthError is correctly raised when
    items of an incorrect size are given"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectLengthError):
        CiscoWLCAPIValidators.length(length_test_a, size=2)
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectLengthError):
        CiscoWLCAPIValidators.length(length_test_b, size=8)
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectLengthError):
        CiscoWLCAPIValidators.length(length_test_c, size=5)


def test_length_correct():
    """Test that the length validator correctly validates
    items of the correct length"""
    assert CiscoWLCAPIValidators.length(length_test_a, size=4)
    assert CiscoWLCAPIValidators.length(length_test_b, size=5)
    assert CiscoWLCAPIValidators.length(length_test_c, size=4)


def test_credential_type_fails():
    """Test that an IncorrectTypeError is correctly raised
    when the credentials parameter is of an incorrect type"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential("admin, password")
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential(['admin', 'password'])
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential({
            'username': 'admin',
            'password': 'password',
        })


def test_credential_length_fails():
    """Test that the credentials tuple length validation correctly
    raises an IncorrectLengthError when there are too few or too many
    items in the tuple"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectLengthError):
        CiscoWLCAPIValidators.credential(('username',))
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectLengthError):
        CiscoWLCAPIValidators.credential(('username','password','extra'))


def test_credential_tuple_type_fails():
    """Test that the credentials tuple validation correctly raises
    an IncorrectTypeError when the tuple contains incorrect types"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential((int(2), int(3)))
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential(('2', int(3)))
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.credential((int(2), '3'))


def test_credential_succeeds():
    """Test that the credentials validator correctly accepts
    valid input"""
    assert CiscoWLCAPIValidators.credential(('admin','password'))


def test_response_code_wrong_response_type():
    """Test that an IncorrectTypeError is correctly raised
    when a Response object is not supplied"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.response_code({})


def test_response_code_wrong_expect_type():
    """"Test that an IncorrectTypeError is correctly raised
    when an incorrect typed parameter is supplied"""
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.response_code(response_test_a, '200')
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.response_code(response_test_a, int(200))
    with pytest.raises(CiscoWLCAPIExceptions.IncorrectTypeError):
        CiscoWLCAPIValidators.response_code(response_test_a, (int(200), '200',))


def test_response_code_unexpected_response_code():
    """Test that an exception is correctly raised when an
    unexpected response code is returned"""
    with pytest.raises(CiscoWLCAPIExceptions.UnexpectedResponseStatusError):
        CiscoWLCAPIValidators.response_code(response_test_a, expect=(401, 503))


def test_response_code_expected_response_code():
    """Tests that the (simulated) response code validates correctly"""
    assert CiscoWLCAPIValidators.response_code(response_test_a)
    assert CiscoWLCAPIValidators.response_code(response_test_b, expect=(200, 401))
    assert CiscoWLCAPIValidators.response_code(response_test_c, expect=(503,))
