import pytest
from src.cisco_wlc_api import CiscoWLCAPI
import src.cisco_wlc_api.Exceptions as CiscoWLCExceptions


def test_constructor_requires_args():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI()


def test_constructor_requires_non_none_args():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri=None, credentials=None)


def test_constructor_requires_credential_contents():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=())


def test_constructor_requires_credential_size():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=('1',))
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=('1','2','3'))


def test_constructor_validates_arg_types():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri=int(1), credentials=str('1'))


def test_constructor_validates_credential_types():
    with pytest.raises(CiscoWLCExceptions.WLCAssertionException):
        _ = CiscoWLCAPI(base_uri='https://127.0.0.1', credentials=(int(2), ('3',)))
