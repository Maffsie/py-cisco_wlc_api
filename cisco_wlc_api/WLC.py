from . import Models, Endpoints, Decorators
from .Core import CiscoWLCAPISession


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
        assert self.session.get(Endpoints.Dashboard).status_code in (200, 401), \
            f"Unexpected response {self.session.response.status_code} when initiating authentication session"
        assert self.session.get(Endpoints.Dashboard).status_code == 200, \
            f"Unexpected response {self.session.response.status_code} when completing authentication"
        self.authenticated = True
        return self.authenticated

    @property
    @Decorators.authenticate
    def client_count(self) -> int:
        return self.session.get(Endpoints.ClientOverview).json()['total']

    @property
    @Decorators.authenticate
    def clients(self) -> list[Models.Client]:
        count = self.client_count
        # TODO: this should iterate through the JSON array and generate Client objects for each client
        # TODO: this should also call Endpoints.Clients and merge the two sets of data
        return self.session.get(Endpoints.ClientsTable, params={
            "take": count, "pageSize": count,
            "page": 1, "skip": 0,
            "sort[0][field]": "macaddr",
            "sort[0][dir]": "asc"
        }).json()['data']

    @property
    @Decorators.authenticate
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
            bytes_total=x['bytes_total'],
            bytes_last_90=x['bytes_90s']
        ) for x in first['data']+second['data']]

    @Decorators.authenticate
    def get_client(self,
                   name: str = None,
                   ip4: str = None,
                   ip6: str = None,
                   mac: str = None):
        assert len([arg for arg in [name, ip4, ip6, mac] if arg is not None]) == 1, \
            "Exactly one argument must be passed to get_client"
        return
    """
    TODO
    def topapps()
    def client_by_address(name: str = None, ip4: str = None, ip6: str = None, mac: str = None)
    
    """
