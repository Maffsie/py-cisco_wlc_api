from os import environ as env
from src.cisco_wlc_api import CiscoWLCAPI
import src.cisco_wlc_api.Endpoints as Endpoints

wlc = CiscoWLCAPI(
    base_uri=env.get('WLC_URI'),
    credentials=(
        env.get('WLC_USER', 'admin'),
        env.get('WLC_PASS')
    )
)

for client in wlc.clients:
    print(f"{client.Hostname} = {client.IP4}")
