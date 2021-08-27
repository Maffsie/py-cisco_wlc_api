"""
Tests pertaining to the constructor for cisco_wlc_api.WLC.CiscoWLCAPI
"""

# pylint: disable=import-error
import pytest
from src.cisco_wlc_api import CiscoWLCAPI
import src.cisco_wlc_api.Exceptions as CiscoWLCExceptions


def test_constructor_requires_args():
    """Test that the constructor correctly raises an exception
    when there are no arguments"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI()


def test_constructor_requires_non_none_args():
    """Test that the constructor correctly raises an exception
    when the arguments are None"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri=None, credentials=None)


def test_constructor_requires_credential_contents():
    """Test that the constructor correctly raises an exception
    when the credentials tuple is empty"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=())


def test_constructor_requires_credential_size():
    """Test that the constructor correctly raises an exception
    when the credentials tuple is of an incorrect size"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=('1',))
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=('1', '2', '3'))


def test_constructor_validates_arg_types():
    """Test that the constructor correctly raises an exception
    when the arguments are of an incorrect type"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri=int(1), credentials=str('1'))


def test_constructor_validates_credential_types():
    """Test that the constructor correctly raises an exception
    when the credentials tuple contains incorrect types"""
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=(int(2), ('3',)))
