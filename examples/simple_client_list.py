"""
Simple test script to list the hostname and IP address of all
associated wireless clients.
Credentials are gathered from environment variables.
"""

from os import environ as env

# pylint: disable=import-error
from src.cisco_wlc_api import CiscoWLCAPI

WLC = CiscoWLCAPI(
    base_uri=env.get("WLC_URI"),
    credentials=(env.get("WLC_USER", "admin"), env.get("WLC_PASS")),
)

if __name__ == "__main__":
    for client in WLC.clients:
        print(f"{client.Hostname} = {client.IP4}")
    c = WLC.clients[0]
    c.refresh()
    apps = c.apps
    print(f"{c.Hostname}: {len(apps)} app(s)")
    for app in apps:
        print(f"{app.Name}: {app.BytesTotal}b")
