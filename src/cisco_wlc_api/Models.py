from .Core import CiscoWLCAPISession
from . import Endpoints, Enums
from cachetools.func import ttl_cache


class Application:
    def __init__(self,
                 name: str,
                 icon: str,
                 bytes_total: int,
                 bytes_last_90: int
                 ):
        self.Name = name
        self.Icon = icon
        self.BytesTotal = bytes_total
        self.BytesRecently = bytes_last_90

    def __add__(self, other):
        return self.BytesTotal + other.BytesTotal

    def __sub__(self, other):
        if self.BytesTotal >= other.BytesTotal:
            return self.BytesTotal - other.BytesTotal
        else:
            return other.BytesTotal - self.BytesTotal

    def __repr__(self):
        return f"<Application {self.Name} (total {self.BytesTotal}b, {self.BytesRecently} last 90 seconds)>"


class Client:
    def __init__(self,
                 session: CiscoWLCAPISession,
                 macaddr: str,
                 ip4: str = None,
                 ip6: str = None,
                 hostname: str = None,
                 icon: str = None,
                 devtype: str = None,
                 ):
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
        self.rf_spatial = None
        self.rf_spatial_max = None
        self.rf_channel = None
        self.rf_capability = None

        self.security_acl_v4 = None
        self.security_acl_v6 = None
        self.security_cipher = None
        self.security_kmp = None
        self.security_policy = None

        self._last_refresh = None
        self._last_rf = None

    def __repr__(self):
        return f"<Wireless client (MAC={self.MAC})>"

    def refresh(self):
        self.refresh_network()
        self.refresh_qos()
        self.refresh_security()

    def refresh_network(self):
        attrs = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.Network,
                                     data=self._session.get(
                                         Endpoints.Clients.Client.Network,
                                         params={
                                             "deviceMacAddress": self.MAC
                                         }).json()['data'])
        self.IP4 = attrs['IP4']
        self.IP6 = attrs['IP6']
        self.VLAN = int(attrs['VLAN'])
        self.is_fastlane = attrs['is_fastlane']
        self.mobility_role = attrs['mobility_role']

    def refresh_qos(self):
        attrs = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.QoS,
                                     data=self._session.get(
                                         Endpoints.Clients.Client.QoS,
                                         params={
                                             "deviceMacAddress": self.MAC
                                         }).json()['data'])
        self.qos_wmm = attrs['wmm']
        self.qos_apsd = attrs['apsd']
        self.qos_level = attrs['level']

    def refresh_rf(self):
        attrs = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.RF,
                                     data=self._session.get(
                                         Endpoints.Clients.Client.RF,
                                         params={
                                             "deviceMacAddress": self.MAC
                                         }).json()['data'])


    def refresh_security(self):
        attrs = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.Security,
                                     data=self._session.get(
                                         Endpoints.Clients.Client.Security,
                                         params={
                                             "deviceMacAddress": self.MAC
                                         }).json()['data'])
        (self.security_acl_v4, self.security_acl_v6) = attrs['sec_acl'].split('/')
        self.security_cipher = attrs['sec_cipher']
        self.security_kmp = attrs['sec_kmp']
        self.security_policy = attrs['sec_pol']

    @property
    @ttl_cache(ttl=60)
    def associated(self):
        self.refresh_rf()

    @property
    @ttl_cache(ttl=60)
    def link_state(self):
        self.refresh_rf()
        return [attr['value'] for attr in self._last_rf if attr['key'] == "Capabilities"][0]


"""
Client:
# From data/clients.html
- MAC Address
- Icon String
- Device Type
- Bytes Total
- Bytes (last 90 seconds)
# From data/client-table.html
- Hostname
- Protocol
- IP Address
- Associated SSID
- RSSI
- Time Online
- Link Speed
- State

Method-based properties
# From data/rfdashboard/clientview_topapps.html
Apps[]:
- Name
- Bytes Total
- Percentage of total client activity

# From data/rfdashboard/clientview_details.html
- Associated to AP
- Channel
- Capabilities
- CCXV?
- Spatial stream count
- Link Speed
- RSSi
- SnR
- Max link speed
- Channel width

# From data/rfdashboard/clientview_details_network.html
- IPv4 address
- IPv6 address
- VLAN
- Source group tag
- Fastlane status
- Mobility role

# From data/rfdashboard/clientview_details_security.html
- Security Policy
- Security Cipher
- Key management type
- EAP type
- Applied ACLs
- mDNS profile
- AAA role

# From data/rfdashboard/clientview_details_qos.html
- WMM
- U-APSD
- QoS Level
"""
