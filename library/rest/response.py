import json
import requests

class Response:
    """Provides an abstraction of a REST API response object."""

    status_code = None
    headers = None
    payload = None
    payload_parsed = None
    json = None

    def __init__(self, status_code=None, headers=None, payload=None, parse_payload=False):
        """Initializing a response object.
        Can optionally provide the details for status code, headers and payload."""
        if status_code:
            self.set_status_code(status_code)
        if None != headers:
            self.set_headers(headers)
        if payload:
            self.set_payload(payload, parse_payload)

    def set_status_code(self, status_code):
        """Setter for the status_code property."""
        if False == isinstance(status_code, int):
            raise Exception("Status code should be an integer!")
        if status_code < 0:
            # TODO: Might want to improve the valid status code check
            raise Exception("Unsupported value provided for status code: {}!".format(status_code))
        self.status_code = status_code
        return self

    def set_headers(self, headers):
        """Setter for the headers property."""
        if False == isinstance(headers, requests.structures.CaseInsensitiveDict):
            raise Exception("Headers are supported only as a dictionary! {} provided".format(type(headers)))
        self.headers = headers
        return self

    def set_payload(self, payload, parse=True):
        """Setter for the payload property.
        Optionally can omit parsingthe payload for specific cases we'd like to do this on demand.
        As an example - if the payload is too large and we'd like to parse it in an async task
        and not in the main portion of the execution.
        Throws a json.decoder.JSONDecodeError in case of invalid JSON payload provided."""
        self.payload = payload
        self.payload_parsed = parse
        if True == parse:
            self.json = json.loads(payload)
        return self

    def get_json(self, refresh=False):
        """Getter for the parsed payload data.
        Supports an argument for refreshing the valu - forcing parsing the payload again.
        Throws a json.decoder.JSONDecodeError in case of invalid JSON payload provided."""
        if refresh and None != self.payload:
            self.json = json.loads(self.payload)
        return self.json
