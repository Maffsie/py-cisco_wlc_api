# Authentication-related
Dashboard = "screens/dashboard.html"


class APs:
    List = "data/aps.html"
    List24 = "data/ap-attributes-slot0.html"
    List5 = "data/ap-attributes-slot1.html"

    class AP:
        Get = "data/rfdashboard/apview_general.html"


class Clients:
    Counts = "screens/webui/resource/spartan/clientDetails.json"
    List = "data/client-table.html"

    class Client:
        RF = "data/rfdashboard/clientview_details.html"
        Apps = "data/rfdashboard/clientview_topapps.html"
        Mobility = "data/rfdashboard/clientview_mobility_data.html"
        Network = "data/rfdashboard/clientview_details_network.html"
        Security = "data/rfdashboard/clientview_details_security.html"
        QoS = "data/rfdashboard/clientview_details_qos.html"


class RF:
    List = "data/wlans.html"
    AVCProfile = "data/avc_profile_status.html"

    class Performance:
        ClientStats = "data/rfdashboard/clientperformance_clienttable.html"


class System:
    Status = "data/system1.html"
    Info = "data/system_information.html"


class WidgetSources:
    Apps = "data/apps.html"
    Clients = "data/clients.html"
    OperatingSystems = "data/oss.html"
