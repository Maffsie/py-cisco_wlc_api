# pylint: disable=invalid-name

"""
Module core. Contains classes that are critical to the operation of this module
Currently this includes CiscoWLCAPISession, which inherits the Requests.Session object
"""

import requests

from . import Exceptions, Validators


class CiscoWLCAPISession(requests.Session):
    """requests.Session subclass with methods specifically for dealing with requests
    to the Cisco WLC web interface"""

    # wah wah i'm python i cry when there are three friggin' arguments
    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        *args,
        base_uri: str = "",
        credentials: tuple = None,
        verify_tls: bool = True,
        **kwargs,
    ):
        """
        Requests.Session object with method changes specific to the Cisco WLC's API
        :param args:
        Positional arguments passed directly to the Requests.Session constructor
        :param base_uri:
        A URI corresponding to the base address of a Cisco WLC, including protocol,
        but NOT any sub-paths or trailing slashes
        :param credentials:
        A tuple containing a string with the administrator username and a string with
        the corresponding password
        :param verify_tls:
        A boolean indicating whether the TLS certificate should be verified.
        This defaults to false.
        :param kwargs:
        Keyword arguments passed directly to the Requests.Session constructor
        """
        super().__init__(*args, **kwargs)
        Validators.baseurl(base_uri)
        self._base_uri = base_uri
        Validators.credential(credentials)
        self.auth = credentials
        self._last_url = None
        self._last_method = None
        self._last_kwargs = None
        self.authed = False
        self.response = None

        if not verify_tls:
            self.verify = False
            # no-member because pylint doesn't see the urllib3 import from requests
            #  but it's disabled here because requests literally can't work without
            #  urllib3, so it -will- be there
            # pylint: disable=no-member
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )

    def retry_last(self) -> requests.Response:
        """
        Simple function to perform the most recently-performed request again
        :return:
        A Requests.Response object with the response data
        """
        Validators.simple(
            condition=self._last_url is not None,
            message_on_failure="No previous request to retry.",
            message_for_remediation="Make a request first",
            exception_type=Exceptions.NoPreviousRequestError,
        )
        return self.request(
            method=self._last_method, url=self._last_url, **self._last_kwargs
        )

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        """
        Constructs a Requests.Request object with the given method and endpoint, performs
        it and then returns the resulting Requests.Response object
        :param method:
        HTTP method to perform the request using, such as 'GET' or 'POST'
        :param url:
        Cisco WLC API endpoint to perform the request against, relative to the base URL.
        This should be a string from the cisco_wlc_api.Endpoints class
        :param args:
        Positional arguments passed directly to Requests.request()
        :param kwargs:
        Keyword arguments passed directly to Requests.request()
        :return:
        A Requests.Response object with the response data
        """

        self._last_url = url
        self._last_method = method
        self._last_kwargs = kwargs
        self.response = super().request(
            method=method, url=f"{self._base_uri}/{url}", *args, **kwargs
        )
        if self.response.status_code == 401:
            if self.authed:
                self.authed = False
                raise PermissionError(
                    "Session authentication has timed out. Please log-in again and retry."
                )
            self.authed = False
        return self.response

    def map_kv(self, mapper: dict, data: list = None):
        """
        Maps a key-value list from the Cisco WLC to a list of dict attributes
        :param mapper:
        A dict where each key is the name of the key in the WLC's response, and its value is
        what key the value will have in the returned dict
        :param data:
        A list of dicts which each contain a key and a value as separate attributes, usually
        returned from the Cisco WLC's API
        :return:
        A dict with the resulting key-value mapping
        """

        retdict = {}
        if data is None and self.response.json().get("data", None) is None:
            raise Exceptions.QueryReturnedNoResultsError()
        for item in data if data is not None else self.response.json()["data"]:
            (k, v) = (item["key"], item["value"])
            if k in mapper.keys():
                if str(v).lower() in ("no", "false"):
                    v = False
                if str(v).lower() in ("yes", "true"):
                    v = True
                if str(v).lower() in ("unknown", "unclassified"):
                    v = None
                retdict[mapper.get(k)] = v
        return retdict
