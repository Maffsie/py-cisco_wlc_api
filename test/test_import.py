"""
Tests pertaining to basic imports
"""


def test_simple_import():
    """Test that the module base can be imported"""
    # pylint: disable=unused-import,import-outside-toplevel,import-error
    import src.cisco_wlc_api


def test_simple_class_import():
    """Test that the primary class can be imported"""
    # pylint: disable=unused-import,import-outside-toplevel,import-error
    from src.cisco_wlc_api import CiscoWLCAPI
