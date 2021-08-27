from . import (
    Endpoints,
    Models,
    Validators
)
from .Core import CiscoWLCAPISession
from .Decorators import must_auth


class CiscoWLCAPI:
    def __init__(self,
                 base_uri: str = "",
                 credentials: tuple = None,
                 verify_tls: bool = False):
        self.session = CiscoWLCAPISession(
            base_uri=base_uri,
            credentials=credentials,
            verify_tls=verify_tls
        )
        self.authenticated = False

    def login(self):
        self.authenticated = False
        Validators.response_code(response=self.session.get(Endpoints.Dashboard), expect=(200, 401))
        Validators.response_code(response=self.session.retry_last())
        self.authenticated = True
        return self.authenticated

    @property
    @must_auth
    def client_count(self) -> int:
        return self.session.get(Endpoints.Clients.Counts).json()['total']

    @property
    @must_auth
    def clients(self) -> list[Models.Client]:
        count = self.client_count
        # TODO: this should iterate through the JSON array and generate Client objects for each client
        # TODO: this should also call Endpoints.Clients and merge the two sets of data
        clients = []
        for client in self.session.get(Endpoints.Clients.List, params={
            "take": count, "pageSize": count,
            "page": 1, "skip": 0,
            "sort[0][field]": "macaddr",
            "sort[0][dir]": "asc"
        }).json()['data']:
            clients.append(Models.Client(
                session=self.session,
                macaddr=client['macaddr'],
                hostname=client['HN'],
                ip4=client['IP'],
                devtype=client['devtype']
            ))
        return clients

    @property
    @must_auth
    def top_apps(self) -> list[Models.Application]:
        first = self.session.get(Endpoints.Apps, params={
            "take": 150, "pageSize": 150,
            "page": 1, "skip": 0,
            "sort[0][field]": "bytes_90s",
            "sort[0][dir]": "desc",
            "sort[1][field]": "bytes_total",
            "sort[1][dir]": "desc"
        }).json()
        remainder = first['total'] - 150
        if remainder <= 0:
            return first['data']
        second = self.session.get(Endpoints.Apps, params={
            "take": remainder, "pageSize": 150,
            "page": 1, "skip": 150,
            "sort[0][field]": "bytes_90s",
            "sort[0][dir]": "desc",
            "sort[1][field]": "bytes_total",
            "sort[1][dir]": "desc"
        }).json()
        return [Models.Application(
            name=x['name'],
            icon=x['icon_type'],
            bytes_total=int(x['bytes_total']),
            bytes_last_90=int(x['bytes_90s'])
        ) for x in first['data']+second['data']]

    @must_auth
    def get_client(self,
                   name: str = None,
                   ip4: str = None,
                   ip6: str = None,
                   mac: str = None):
        Validators.length([arg for arg in [name, ip4, ip6, mac] if arg is not None], 1)
        return
    """
    TODO
    def topapps()
    def client_by_address(name: str = None, ip4: str = None, ip6: str = None, mac: str = None)
    
    """
