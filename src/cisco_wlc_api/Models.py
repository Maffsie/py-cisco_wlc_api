# pylint: disable=invalid-name

"""
Models related to the data returned by WLC API requests
"""

from cachetools.func import ttl_cache

# I don't know why pylint will inconsistently report an import issue error
# pylint: disable=relative-beyond-top-level
from . import Endpoints, Exceptions
from .Core import CiscoWLCAPISession


class Application:
    """Model representing a single 'application' returned by an API request"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: str,
        bytes_total: int,
        session: CiscoWLCAPISession,
        mac_address: str = None,
        icon: str = None,
        bytes_last_90: int = None,
    ):
        self.Name = name
        self.Icon = icon
        self.BytesTotal = bytes_total
        self.BytesRecently = bytes_last_90
        self.MAC = mac_address
        self._session = session

        self._last = {
            "client_apps": {},
            "network_apps": {},
        }

    def __add__(self, other):
        return self.BytesTotal + other.BytesTotal

    def __sub__(self, other):
        if self.BytesTotal >= other.BytesTotal:
            return self.BytesTotal - other.BytesTotal
        return other.BytesTotal - self.BytesTotal

    def __repr__(self):
        bytes_t = self.BytesTotal
        units = "b"
        # i looked on stackoverflow for better ways of doing this
        #  and everything was more complicated
        #  so fuck that
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = "kb"
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = "mb"
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = "gb"
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = "tb"
        return (
            f"<Application (Name={self.Name}, total={bytes_t:g}{units},"
            f"recent={self.BytesRecently if self.BytesRecently is not None else '[no data]'}b)>"
        )

    @ttl_cache(ttl=60)
    def refresh(self):
        """Refreshes the Application data if possible"""
        if self.MAC is None:
            self._refresh_global_app()
        else:
            self._refresh_client_app()

    @ttl_cache(ttl=60)
    def _refresh_client_app(self):
        # This query isn't filtered serverside; Cisco just..didn't write the code to
        #  do the filtering.
        self._last["client_apps"] = self._session.get(
            Endpoints.Clients.Client.Apps,
            params={
                "deviceMacAddress": self.MAC,
                "take": 1,
                "pageSize": 1,
                "page": 1,
                "skip": 0,
                "sort[0][field]": "bytes_total",
                "sort[0][dir]": "desc",
            },
        ).json()["data"]
        self._last["client_apps"] = list(
            filter(lambda app: app["name"] == self.Name, self._last["client_apps"])
        )
        if len(self._last["client_apps"]) != 1:
            raise Exceptions.UnexpectedResponseValueError(
                "Expected one result in client_apps refresh, but got"
                f"{len(self._last['client_apps'])} instead"
            )
        self._last["client_apps"] = self._last["client_apps"][0]
        self.BytesTotal = self._last["client_apps"].get("bytes_total", self.BytesTotal)

    @ttl_cache(ttl=60)
    def _refresh_global_app(self):
        self._last["network_apps"] = self._session.get(
            Endpoints.WidgetSources.Apps,
            params={
                "take": 1,
                "pageSize": 1,
                "page": 1,
                "skip": 0,
                "sort[0][field]": "bytes_total",
                "sort[0][dir]": "desc",
                "filter[logic]": "and",
                "filter[filters][0][field]": "name",
                "filter[filters][0][operator]": "eq",
                "filter[filters][0][value]": self.Name,
            },
        ).json()["data"]
        if len(self._last["network_apps"]) != 1:
            raise Exceptions.UnexpectedResponseValueError(
                "Expected one result in network_apps refresh, but got"
                f"{len(self._last['network_apps'])} instead"
            )
        self._last["network_apps"] = self._last["network_apps"][0]
        self.BytesTotal = self._last["network_apps"].get("bytes_total", self.BytesTotal)
        self.BytesRecently = self._last["network_apps"].get(
            "bytes_90s", self.BytesRecently
        )


class Client:
    """Model representing a Client associated to the WLC in some way"""

    # pylint: disable=too-many-instance-attributes,too-many-arguments
    def __init__(
        self,
        session: CiscoWLCAPISession,
        macaddr: str,
        ip4: str = None,
        ip6: str = None,
        hostname: str = None,
        icon: str = None,
        devtype: str = None,
    ):
        """
        Model representing a Client associated to the WLC
        :param session:
        Mandatory, a CiscoWLCAPISession object provided from the caller
        :param macaddr:
        MAC address of the client
        :param ip4:
        IPv4 address of the client
        :param ip6:
        IPv6 address of the client
        :param hostname:
        Hostname (either DNS or DHCP) of the client
        :param icon:
        Name of a UI icon representing the client device type
        :param devtype:
        Type of client device, determined via association data or MAC address
        """
        self._session = session
        self.MAC = macaddr
        self.IP4 = ip4
        self.IP6 = ip6
        self.Hostname = hostname
        self.Icon = icon
        self.Type = devtype

        self.VLAN = None
        self.is_fastlane = None
        self.mobility_role = None

        self.qos_wmm = None
        self.qos_apsd = None
        self.qos_level = None

        self.rf_width = None
        self.rf_width_max = None
        self.rf_rate = None
        self.rf_spatial_streams = None
        self.rf_spatial_streams_max = None
        self.rf_channel = None
        self.rf_capability = None
        self.rf_rssi = None
        self.rf_snr = None
        self.rf_connection_score = None

        self.security_acl_v4 = None
        self.security_acl_v6 = None
        self.security_cipher = None
        self.security_kmp = None
        self.security_policy = None

        self._last = {
            "apps": [],
            "mobility": [],
            "network": {},
            "qos": {},
            "rf": {},
            "security": {},
        }

    def __repr__(self):
        return f"<Wireless client (MAC={self.MAC})>"

    @ttl_cache(ttl=60)
    def refresh(self):
        """Refreshes all data related to the client"""
        self.refresh_apps()
        self.refresh_mobility()
        self.refresh_network()
        self.refresh_qos()
        self.refresh_rf()
        self.refresh_security()

    @ttl_cache(ttl=60)
    def refresh_apps(self):
        """Refreshes the application-specific bandwidth usage data"""
        self._last["apps"] = self._session.get(
            Endpoints.Clients.Client.Apps,
            params={
                "deviceMacAddress": self.MAC,
                "take": 50,
                "pageSize": 200,
                "page": 1,
                "skip": 0,
                "sort[0][field]": "bytes_total",
                "sort[0][dir]": "desc",
            },
        ).json()["data"]

    @ttl_cache(ttl=60)
    def refresh_mobility(self):
        """Refreshes the Cisco Mobility-related data for the client"""
        self._last["mobility"] = self._session.get(
            Endpoints.Clients.Client.Mobility, params={"deviceMacAddress": self.MAC}
        ).json()["mobility"]

    @ttl_cache(ttl=60)
    def refresh_network(self):
        """Refreshes the network-related data for the client"""
        self._last["network"] = self._session.map_kv(
            mapper=Endpoints.Clients.Client.Maps.Network,
            data=self._session.get(
                Endpoints.Clients.Client.Network, params={"deviceMacAddress": self.MAC}
            ).json()["data"],
        )
        self.IP4 = self._last["network"]["IP4"]
        self.IP6 = self._last["network"]["IP6"]
        self.VLAN = int(self._last["network"]["VLAN"])
        self.is_fastlane = self._last["network"]["is_fastlane"]
        self.mobility_role = self._last["network"]["mobility_role"]

    @ttl_cache(ttl=60)
    def refresh_qos(self):
        """Refreshes the QoS-related data for the client"""
        self._last["qos"] = self._session.map_kv(
            mapper=Endpoints.Clients.Client.Maps.QoS,
            data=self._session.get(
                Endpoints.Clients.Client.QoS, params={"deviceMacAddress": self.MAC}
            ).json()["data"],
        )
        self.qos_wmm = self._last["qos"]["wmm"]
        self.qos_apsd = self._last["qos"]["apsd"]
        self.qos_level = self._last["qos"]["level"]

    @ttl_cache(ttl=60)
    def refresh_rf(self):
        """Refreshes the RF-related data for the client"""
        self._last["rf"] = self._session.map_kv(
            mapper=Endpoints.Clients.Client.Maps.RF,
            data=self._session.get(
                Endpoints.Clients.Client.RF, params={"deviceMacAddress": self.MAC}
            ).json()["data"],
        )
        self.rf_width = int(self._last["rf"]["chanwidth"])
        self.rf_width_max = int(self._last["rf"]["chanwidth_max"])
        self.rf_rate = int(self._last["rf"]["assocrate"])
        self.rf_spatial_streams = int(self._last["rf"]["spat_str"])
        self.rf_spatial_streams_max = int(self._last["rf"]["spat_str_max"])
        self.rf_channel = int(self._last["rf"]["chan"])
        self.rf_capability = self._last["rf"]["wlcap"]
        self.rf_rssi = int(self._last["rf"]["strength"])
        self.rf_snr = int(self._last["rf"]["snr"])
        self.rf_connection_score = int(self._last["rf"]["connscore"])

        self.Hostname = self._last["rf"]["host"]
        self.Type = self._last["rf"]["type"]

    @ttl_cache(ttl=60)
    def refresh_security(self):
        """Refreshes the client's security-related data from the WLC"""
        self._last["security"] = self._session.map_kv(
            mapper=Endpoints.Clients.Client.Maps.Security,
            data=self._session.get(
                Endpoints.Clients.Client.Security, params={"deviceMacAddress": self.MAC}
            ).json()["data"],
        )
        (self.security_acl_v4, self.security_acl_v6) = self._last["security"][
            "sec_acls"
        ].split("/")
        self.security_cipher = self._last["security"]["sec_cipher"]
        self.security_kmp = self._last["security"]["sec_kmp"]
        self.security_policy = self._last["security"]["sec_pol"]

    @property
    @ttl_cache(ttl=60)
    def associated(self) -> bool:
        """Returns a boolean indicating whether the client is currently associated"""
        try:
            self.refresh_rf()
        except Exceptions.QueryReturnedNoResultsError:
            return False
        return True

    @property
    @ttl_cache(ttl=60)
    def bytes_total(self) -> int:
        """The total count of bytes transmitted or received by the client"""
        self.refresh_rf()
        return self._last["rf"].get("bytes_total", 0)

    @property
    @ttl_cache(ttl=60)
    def uptime(self) -> int:
        """The time in seconds that a client has been associated to the AP"""
        self.refresh_rf()
        return self._last["rf"].get("assoctime", 0)

    @property
    @ttl_cache(ttl=60)
    def apps(self) -> list[Application]:
        """Fetch application-specific bandwidth usage for this client"""
        self.refresh_apps()
        apps = []
        for app in self._last["apps"]:
            apps.append(
                Application(
                    name=app["name"],
                    bytes_total=int(app["bytes_total"]),
                    session=self._session,
                    mac_address=self.MAC,
                )
            )
        return apps
