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
        return self.get(Endpoints.Clients, params={
            "take": count, "pageSize": count,
            "page": 1, "skip": 0,
            "sort[0][field]": "macaddr",
            "sort[0][dir]": "asc"
        }).json()['data']
