from os import environ as env
from src.cisco_wlc_api import CiscoWLCAPI

wlc = CiscoWLCAPI(
    base_uri=env.get('WLC_URI'),
    credentials=(
        env.get('WLC_USER', 'admin'),
        env.get('WLC_PASS')
    )
)

if __name__ == "__main__":
    for client in wlc.clients:
        print(f"{client.Hostname} = {client.IP4}")
