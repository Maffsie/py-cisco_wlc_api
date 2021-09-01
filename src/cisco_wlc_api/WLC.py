# pylint: disable=invalid-name

"""
Primary class for the cisco_wlc_api module
"""

from . import Endpoints, Models, Validators
from .Core import CiscoWLCAPISession
from .Decorators import must_auth


class CiscoWLCAPI:
    """
    Class for interacting with the Cisco WLC's API in a user-friendly way
    """

    def __init__(
        self, base_uri: str = "", credentials: tuple = None, verify_tls: bool = False
    ):
        """
        Creates a CiscoWLCAPI object
        :param base_uri:
        Base URI of the Cisco WLC's web interface, including protocol, but
        excluding any sub-paths or trailing slashes
        :param credentials:
        Tuple containing two strings, one the username and one the password
        :param verify_tls:
        Boolean indicating whether TLS certificates should be checked;
        defaults to disabled
        """
        self.session = CiscoWLCAPISession(
            base_uri=base_uri, credentials=credentials, verify_tls=verify_tls
        )
        self.authenticated = False

    def login(self):
        """Attempts to authenticate with the WLC"""
        self.authenticated = False
        Validators.response_code(
            response=self.session.get(Endpoints.Dashboard), expect=(200, 401)
        )
        Validators.response_code(response=self.session.retry_last())
        self.authenticated = True
        return self.authenticated

    @property
    @must_auth
    def client_count(self) -> int:
        """The number of clients currently associated to the WLC"""
        return int(self.session.get(Endpoints.Clients.Counts).json()["total"])

    @property
    @must_auth
    def clients(self) -> list[Models.Client]:
        """A list of all clients currently associated to the WLC"""
        count = self.client_count
        clients = []
        for client in self.session.get(
            Endpoints.Clients.List,
            params={
                "take": count,
                "pageSize": count,
                "page": 1,
                "skip": 0,
                "sort[0][field]": "macaddr",
                "sort[0][dir]": "asc",
            },
        ).json()["data"]:
            clients.append(
                Models.Client(
                    session=self.session,
                    macaddr=client["macaddr"],
                    hostname=client["HN"],
                    ip4=client["IP"],
                    devtype=client["devtype"],
                )
            )
        return clients

    # @property
    # @must_auth
    # def top_apps(self) -> list[Models.Application]:
    #    """A list of application-specific bandwidth information"""
    #    first = self.session.get(
    #        Endpoints.Apps,
    #        params={
    #            "take": 150,
    #            "pageSize": 150,
    #            "page": 1,
    #            "skip": 0,
    #            "sort[0][field]": "bytes_90s",
    #            "sort[0][dir]": "desc",
    #            "sort[1][field]": "bytes_total",
    #            "sort[1][dir]": "desc",
    #        },
    #    ).json()
    #    remainder = first["total"] - 150
    #    if remainder <= 0:
    #        return first["data"]
    #    second = self.session.get(
    #        Endpoints.Apps,
    #        params={
    #            "take": remainder,
    #            "pageSize": 150,
    #            "page": 1,
    #            "skip": 150,
    #            "sort[0][field]": "bytes_90s",
    #            "sort[0][dir]": "desc",
    #            "sort[1][field]": "bytes_total",
    #            "sort[1][dir]": "desc",
    #        },
    #    ).json()
    #    return [
    #        Models.Application(
    #            name=x["name"],
    #            icon=x["icon_type"],
    #            bytes_total=int(x["bytes_total"]),
    #            bytes_last_90=int(x["bytes_90s"]),
    #        )
    #        for x in first["data"] + second["data"]
    #    ]
