from .Core import CiscoWLCAPISession
from . import Endpoints, Enums
from cachetools.func import ttl_cache


class Application:
    def __init__(self,
                 name: str,
                 bytes_total: int,
                 icon: str = None,
                 bytes_last_90: int = None
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
        bytes_t = self.BytesTotal
        units = 'b'
        # TODO: This is really gross lmfao
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = 'kb'
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = 'mb'
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = 'gb'
        if bytes_t >= 1024:
            bytes_t /= 1024
            units = 'tb'
        return (f"<Application (Name={self.Name}, total={bytes_t:g}{units},"
                f"recent={self.BytesRecently if self.BytesRecently is not None else '[no data]'}b)>")


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
            'apps': [],
            'mobility': [],
            'network': {},
            'qos': {},
            'rf': {},
            'security': {}
        }

    def __repr__(self):
        return f"<Wireless client (MAC={self.MAC})>"

    @ttl_cache(ttl=60)
    def refresh(self):
        self.refresh_network()
        self.refresh_qos()
        self.refresh_rf()
        self.refresh_security()

    @ttl_cache(ttl=60)
    def refresh_apps(self):
        self._last['apps'] = self._session.get(
            Endpoints.Clients.Client.Apps,
            params={
                "deviceMacAddress": self.MAC,
                "take": 50,
                "pageSize": 200,
                "page": 1,
                "skip": 0,
                "sort[0][field]": "bytes_total",
                "sort[0][dir]": "desc"
            }).json()['data']

    @ttl_cache(ttl=60)
    def refresh_mobility(self):
        self._last['mobility'] = self._session.get(
            Endpoints.Clients.Client.Mobility,
            params={
                "deviceMacAddress": self.MAC
            }).json()['mobility']

    @ttl_cache(ttl=60)
    def refresh_network(self):
        self._last['network'] = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.Network,
                                                     data=self._session.get(
                                                         Endpoints.Clients.Client.Network,
                                                         params={
                                                             "deviceMacAddress": self.MAC
                                                         }).json()['data'])
        self.IP4 = self._last['network']['IP4']
        self.IP6 = self._last['network']['IP6']
        self.VLAN = int(self._last['network']['VLAN'])
        self.is_fastlane = self._last['network']['is_fastlane']
        self.mobility_role = self._last['network']['mobility_role']

    @ttl_cache(ttl=60)
    def refresh_qos(self):
        self._last['qos'] = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.QoS,
                                                 data=self._session.get(
                                                     Endpoints.Clients.Client.QoS,
                                                     params={
                                                         "deviceMacAddress": self.MAC
                                                     }).json()['data'])
        self.qos_wmm = self._last['qos']['wmm']
        self.qos_apsd = self._last['qos']['apsd']
        self.qos_level = self._last['qos']['level']

    @ttl_cache(ttl=60)
    def refresh_rf(self):
        self._last['rf'] = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.RF,
                                     data=self._session.get(
                                         Endpoints.Clients.Client.RF,
                                         params={
                                             "deviceMacAddress": self.MAC
                                         }).json()['data'])
        self.rf_width = int(self._last['rf']['chanwidth'])
        self.rf_width_max = int(self._last['rf']['chanwidth_max'])
        self.rf_rate = int(self._last['rf']['assocrate'])
        self.rf_spatial_streams = int(self._last['rf']['spat_str'])
        self.rf_spatial_streams_max = int(self._last['rf']['spat_str_max'])
        self.rf_channel = int(self._last['rf']['chan'])
        self.rf_capability = self._last['rf']['wlcap']
        self.rf_rssi = int(self._last['rf']['strength'])
        self.rf_snr = int(self._last['rf']['snr'])
        self.rf_connection_score = int(self._last['rf']['connscore'])

        self.Hostname = self._last['rf']['host']
        self.Type = self._last['rf']['type']

    @ttl_cache(ttl=60)
    def refresh_security(self):
        self._last['security'] = self._session.map_kv(mapper=Endpoints.Clients.Client.Maps.Security,
                                                      data=self._session.get(
                                                          Endpoints.Clients.Client.Security,
                                                          params={
                                                              "deviceMacAddress": self.MAC
                                                          }).json()['data'])
        (self.security_acl_v4, self.security_acl_v6) = self._last['security']['sec_acls'].split('/')
        self.security_cipher = self._last['security']['sec_cipher']
        self.security_kmp = self._last['security']['sec_kmp']
        self.security_policy = self._last['security']['sec_pol']

    @property
    @ttl_cache(ttl=60)
    def associated(self):
        self.refresh_rf()

    @property
    @ttl_cache(ttl=60)
    def bytes_total(self):
        self.refresh_rf()
        return self._last['rf'].get('bytes_total', 0)

    @property
    @ttl_cache(ttl=60)
    def uptime(self):
        self.refresh_rf()
        return self._last['rf'].get('assoctime', 0)

    @property
    @ttl_cache(ttl=60)
    def mobility(self):
        self.refresh_mobility()
        return self._last['mobility']

    @property
    @ttl_cache(ttl=60)
    def apps(self):
        self.refresh_apps()
        apps = []
        for app in self._last['apps']:
            apps.append(
                Application(name=app['name'],
                            bytes_total=int(app['bytes_total'])
                            )
            )
        return apps


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
