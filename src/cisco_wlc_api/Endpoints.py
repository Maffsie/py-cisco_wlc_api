# pylint: disable=invalid-name,too-few-public-methods

"""
Abuses the very concept of classes in Python in order to have a reasonably
aesthetically-pleasing list of endpoints
"""

# Authentication-related
Dashboard = "screens/dashboard.html"


class APs:
    """Endpoints related to all APs known to the WLC"""

    List = "data/aps.html"
    List24 = "data/ap-attributes-slot0.html"
    List5 = "data/ap-attributes-slot1.html"

    class AP:
        """Endpoints related to a single AP"""

        Get = "data/rfdashboard/apview_general.html"


class Clients:
    """Endpoints related to all clients known to the WLC"""

    Counts = "screens/webui/resource/spartan/clientDetails.json"
    List = "data/client-table.html"

    class Client:
        """Endpoints related to a single client"""

        RF = "data/rfdashboard/clientview_details.html"
        Apps = "data/rfdashboard/clientview_topapps.html"
        Mobility = "data/rfdashboard/clientview_mobility_data.html"
        Network = "data/rfdashboard/clientview_details_network.html"
        Security = "data/rfdashboard/clientview_details_security.html"
        QoS = "data/rfdashboard/clientview_details_qos.html"

        class Maps:
            """Key-Value mappings for some of the API responses"""

            Network = {
                "IP Address": "IP4",
                "IPv6 Address": "IP6",
                "VLAN": "VLAN",
                "Fastlane Client": "is_fastlane",
                "Mobility Role": "mobility_role",
            }
            QoS = {"WMM": "wmm", "U-APSD": "apsd", "QoS Level": "level"}
            RF = {
                "Hostname": "host",
                "Device Type": "type",
                "Status": "assoctime",
                "SSID": "wlnet",
                "AP Name": "assocap",
                "Channel": "chan",
                "Capabilities": "wlcap",
                "SpatialStream": "spat_str",
                "ConnRate": "assocrate",
                "RSSI": "strength",
                "SNR": "snr",
                "volume": "bytes_total",
                "ConnScore": "connscore",
                "maxClientRate": "rate_max",
                "spatialstrmClients": "spat_str_max",
                "ChannelWidth": "chanwidth",
                "ChannelwidthClient": "chanwidth_max",
            }
            Security = {
                "Policy": "sec_pol",
                "Cipher": "sec_cipher",
                "Key Management": "sec_kmp",
                "ACL (IP/IPv6)": "sec_acls",
            }


class RF:
    """Endpoints related to the RF environment of the WLC deployment"""

    List = "data/wlans.html"
    AVCProfile = "data/avc_profile_status.html"

    class Performance:
        """Endpoints related to RF performance of clients"""

        ClientStats = "data/rfdashboard/clientperformance_clienttable.html"


class System:
    """Endpoints related to the WLC itself"""

    Status = "data/system1.html"
    Info = "data/system_information.html"


class WidgetSources:
    """Endpoints normally called by the widgets on a WLC dashboard,
    these typically contain useful summary data"""

    Apps = "data/apps.html"
    Clients = "data/clients.html"
    OperatingSystems = "data/oss.html"
