import requests


class CiscoWLCAPISession(requests.Session):
    def __init__(self,
                 base_uri: str = "",
                 credentials: tuple = None,
                 verify_tls: bool = True,
                 *args, **kwargs
                 ):
        super(CiscoWLCAPISession, self).__init__(*args, **kwargs)
        assert base_uri.startswith("http"), "base_uri argument must include protocol (http:// or https://)"
        assert not base_uri.endswith("/"), "base_uri must not end with a forward-slash"
        self._base_uri = base_uri
        assert type(credentials) == tuple, "credentials argument must be a tuple"
        assert len(credentials) == 2, "credentials argument must be a username and password"
        self.auth = credentials
        self._last_url = None
        self._last_method = None
        self._last_kwargs = None
        self.authed = False
        self.response = None

        if not verify_tls:
            self.verify = False
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )

    def retry_last(self) -> requests.Response:
        assert self._last_url is not None, "No previous request to retry."
        return self.request(
            method=self._last_method,
            url=self._last_url,
            **self._last_kwargs
        )

    def request(
            self,
            method: str,
            url: str,
            **kwargs
    ) -> requests.Response:
        self._last_url = url
        self._last_method = method
        self._last_kwargs = kwargs
        self.response = super(CiscoWLCAPISession, self).request(
            method=method,
            url=url.format(self._base_uri),
            **kwargs)
        if self.response.status_code == 401:
            if self.authed:
                self.authed = False
                raise PermissionError("Session authentication has timed out. Please log-in again and retry.")
            self.authed = False
        return self.response

