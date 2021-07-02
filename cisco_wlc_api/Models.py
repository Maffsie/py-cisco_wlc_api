"""
App:
- Name
- Icon String
- Bytes Total
- Bytes (last 90 seconds)
"""

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