from abc import ABC, abstractmethod
from base64 import b64encode

class Auth(ABC):
    """Provides an abstraction of an authorization layer for consuming REST API services."""

    credentials = None
    scheme = None

    def __init__(self, credentials=None, scheme=None):
        """Constructor."""
        if None == credentials:
            raise Exception("Credentials are required to instanciate an authorizaion instance!")
        if False == isinstance(credentials, dict):
            raise Exception("Credentials should be provided as a dictionary when instanciating an authorizaion instance!")
        if False == isinstance(scheme, str):
            raise Exception("Authorization scheme needs to be a string value!")

        self.credentials = credentials;
        self.scheme = scheme;

    @abstractmethod
    def decorate_request(request):
        pass

class TokenAuth(Auth):
    """Implements a basic authentication mechanism for consuming REST API services."""

    token = None

    def __init__(self, token, scheme="token"):
        """Constructor."""
        super().__init__({}, scheme)
        if not token:
            raise Exception('Parameter "token" is required!')
        self.token = token

    def decorate_request(self, request):
        """Decorating the headers of a request before executing it - implementing the authorization mechanism."""
        headers = request.headers if request.headers else {}
        headers["Authorization"] = "{} {}".format(self.scheme, self.token)
        return request

class BasicAuth(Auth):
    """Implements a basic authentication mechanism for consuming REST API services."""

    def __init__(self, credentials, scheme="Basic"):
        """Constructor."""
        super().__init__(credentials, scheme)
        if not credentials["user"]:
            raise Exception('Credentials "user" is a required property!')
        if not credentials["password"]:
            raise Exception('Credentials "passwordser" is a required property!')

    def decorate_request(self, request):
        """Decorating the headers of a request before executing it - implementing the authorization mechanism."""
        headers = request.headers if request.headers else {}
        creds = b64encode("{}:{}"
            .format(self.credentials["user"], self.credentials["password"])
            .encode("ascii")
        ).decode("ascii")
        headers["Authorization"] = "{} {}".format(self.scheme, creds)
        return request
