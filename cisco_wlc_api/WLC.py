import requests
from . import Models, Endpoints, Decorators


class CiscoWLCAPI:
    def __init__(self,
                 base_uri: str = "",
                 credentials: tuple = None,
                 verify_tls: bool = False):
        # Argument sanitisation
        assert type(credentials) == tuple, "credentials argument must be a tuple"
        assert len(credentials) == 2, "credentials argument must be a username and password"
        assert base_uri.startswith("http"), "base_uri argument must include protocol (http:// or https://)"
        assert not base_uri.endswith("/"), "base_uri must not end with a forward-slash"

        self.authenticated = False
        self._r = None
        self.base_uri = base_uri
        self.session = requests.Session()
        self.session.auth = credentials

        if not verify_tls:
            self.session.verify = False
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )

    def get(self, uri: str, *args, **kwargs) -> requests.models.Response:
        self._r = self.session.get(uri.format(self.base_uri), *args, **kwargs)
        # Sessions can expire, y'know.
        if self._r.status_code == 401:
            self.authenticated = False
        return self._r

    def login(self):
        self.authenticated = False
        assert self.get(Endpoints.Dashboard).status_code in (200, 401), \
            f"Unexpected response {self._r.status_code} when initiating authentication session"
        assert self.get(Endpoints.Dashboard).status_code == 200, \
            f"Unexpected response {self._r.status_code} when completing authentication"
        self.authenticated = True
        return self.authenticated

    @property
    @Decorators.authenticate
    def client_count(self) -> int:
        return self.get(Endpoints.ClientOverview).json()['total']

    @property
    @Decorators.authenticate
    def clients(self):
        count = self.client_count
        # TODO: this should iterate through the JSON array and generate Client objects for each client
        # TODO: this should also call Endpoints.ClientTable and merge the two sets of data
        return self.get(Endpoints.Clients, params={
            "take": count, "pageSize": count,
            "page": 1, "skip": 0,
            "sort[0][field]": "macaddr",
            "sort[0][dir]": "asc"
        }).json()['data']

    @property
    @Decorators.authenticate
    def top_apps(self):
        first = self.get(Endpoints.Apps, params={
            "take": 150, "pageSize": 150,
            "page": 1, "skip": 0,
            "sort[0][field]": "bytes_total",
            "sort[0][dir]": "desc"
        }).json()
        remainder = first['total'] - 150
        if remainder <= 0:
            return first['data']
        second = self.get(Endpoints.Apps, params={
            "take": remainder, "pageSize": 150,
            "page": 1, "skip": 150,
            "sort[0][field]": "bytes_total",
            "sort[0][dir]": "desc"
        }).json()
        return first['data']+second['data']
    """
    TODO
    def topapps()
    def client_by_address(name: str = None, ip4: str = None, ip6: str = None, mac: str = None)
    
    """
