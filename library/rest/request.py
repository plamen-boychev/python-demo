import json
import enum
import requests
import response

class HTTPVerb(enum.Enum):
    """Provides a list of supported HTTP verbs"""
    get = "GET"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"

    @classmethod
    def is_supported(cls, value):
        return value.value in cls._value2member_map_

class Request:
    """Provides an abstraction of a REST API request object."""

    headers = None
    payload = None
    method = None
    path = None

    def __init__(self, method=None, path=None, payload=None, headers={}):
        """Initializing a request object.
        Can optionally provide the details for path, headers, method and payload."""
        if None != method:
            self.set_method(method)
        if None != path:
            self.set_path(path)
        if None != payload:
            self.set_payload(payload)
        if None != headers:
            self.set_headers(headers)

    def set_method(self, method):
        """Setter for method property. Validates the method value."""
        if False == isinstance(method, HTTPVerb):
            raise Exception("Method should be a string!")
        if False == HTTPVerb.is_supported(method):
            raise Exception('Unsupported method "{}"!'.format(method))
        self.method = method
        return self

    def set_path(self, path):
        if False == isinstance(path, str):
            raise Exception("Value for path should be a string!")
        self.path = path
        return self

    def set_payload(self, payload):
        self.payload = payload
        # TODO: Validate payload injection is available for proper verbs only!
        return self

    def set_headers(self, headers):
        if False == isinstance(headers, dict):
            raise Exception("Value for headers should be a dictionary!")
        if not "Content-Type" in headers:
            headers["Content-Type"] = "application/json"
        self.headers = headers
        return self
    
    def invoke_request(self):
        raw_response = requests.request(self.method.value, self.path, data=self.payload, headers=self.headers, stream=True)
        return response.Response(
            status_code=raw_response.status_code,
            headers=raw_response.headers,
            payload=raw_response.content.decode('UTF-8'),
            parse_payload=False
        )
