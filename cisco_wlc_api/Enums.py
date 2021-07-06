from enum import Enum


class ClientState(Enum):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'


class DeviceType(Enum):
    AppleTV = 'Apple-TV'
    Mac = 'OS_X-Workstation'
    PS3 = 'SonyPS3'
    PS4 = 'SonyPS4'
    XBOX = 'XBOX'
    Misc = 'Unclassified'


class LinkType(Enum):
    A = '802.11a'
    B = '802.11b'
    G = '802.11g'
    N24 = '802.11n'
    N5 = '802.11n'
    AC = '802.11ac'
