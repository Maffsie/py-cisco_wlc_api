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
        return self.BytesTotal+other.BytesTotal

    def __sub__(self, other):
        if self.BytesTotal >= other.BytesTotal:
            return self.BytesTotal-other.BytesTotal
        else:
            return other.BytesTotal-self.BytesTotal

    def __repr__(self):
        return f"<Application {self.Name} (total {self.BytesTotal}b, {self.BytesRecently} last 90 seconds)>"


class Client:
    def __init__(self,
                 session: CiscoWLCAPISession,
                 macaddr: str,
                 ip4: str,
                 ip6: str,
                 hostname: str,
                 icon: str,
                 devtype: str = None,
                 ):
        self._session=session
        self.MAC = macaddr
        self.IP4 = ip4
        self.IP6 = ip6
        self.Hostname = hostname
        self.Icon = icon
        self.Type = devtype

        self._last_rf = None

    def __repr__(self):
        return f"<Wireless client {self.MAC} ({self.IP4}>"

    @property
    @ttl_cache(ttl=60)
    def associated(self):
        self._last_rf = self._session.get(Endpoints.Client.RF, params={
            "deviceMacAddress": self.MAC
        }).json()['data']

    @property
    @ttl_cache(ttl=60)
    def link_state(self):
        self._last_rf = self._session.get(Endpoints.Client.RF, params={
            "deviceMacAddress": self.MAC
        }).json()['data']
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