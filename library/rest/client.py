from abc import ABC, abstractmethod
from library.rest.request import Request, HTTPVerb
from library.rest.auth import Auth
from library.rest.error_handling import ErrorHandler
from library.rest.request import HTTPVerb, Request
from library.rest.response import Response

class RetryCondition(ABC):
    """
    Inheriting classes determine whether or not a request should be re-executed based on custom condition.
    Needs to implement the retry attempts count handling.
    """

    @abstractmethod
    def is_retry_required(response:Response):
        pass

class Client:
    """A base service client class definition.
    Handles communication with a service."""

    base_path = None
    headers = None
    auth = None
    error_handler = None
    retry_condition = None

    def __init__(self, base_path:str, headers:dict=None, auth:Auth=None, error_handler:ErrorHandler=None, retry_condition:RetryCondition=None):
        """Initializing a client."""
        if auth and False == isinstance(auth, Auth):
            raise Exception("Authorization handler needs to be an implementation of Auth class, {} provided".format(type(auth)))
        if error_handler and False == isinstance(error_handler, ErrorHandler):
            raise Exception("Error handler needs to be an implementation of ErrorHandler class, {} provided".format(type(auth)))

        self.base_path = base_path
        self.headers = headers if headers else None
        self.auth = auth if auth else None
        self.error_handler = error_handler if error_handler else ErrorHandler()
        self.retry_condition = retry_condition if retry_condition else None

    def get(self, path:str, headers:dict=None):
        """Execute GET requests."""
        return self.handle_request(path, HTTPVerb.get, headers=headers);

    def post(self, path:str, data:dict, headers:dict=None):
        """Execute POST requests."""
        return self.handle_request(path, HTTPVerb.post, data=data, headers=headers);

    def put(self, path:str, data:dict, headers:dict=None):
        """Execute PUT requests."""
        return self.handle_request(path, HTTPVerb.put, data=data, headers=headers);

    def patch(self, path:str, data:dict, headers:dict=None):
        """Execute PATCH requests."""
        return self.handle_request(path, HTTPVerb.patch, data=data, headers=headers);

    def delete(self, path:str, headers:dict=None):
        """Execute DELETE requests."""
        return self.handle_request(path, HTTPVerb.delete, headers=headers);

    def build_request(self, path:str, method, data:dict=None, headers:dict=None):
        """Creating request objects."""
        full_path = self.base_path + path
        return Request(method, full_path, data, headers)

    def handle_request(self, path:str, method:HTTPVerb, data:dict=None, headers:dict=None):
        """Executing a previously built request object."""
        # Building request
        req = self.build_request(path, method, headers=headers);
        req = req if not self.auth else self.auth.decorate_request(req)

        # Retrieving response
        resp = req.invoke_request()

        # Retry if needed
        while self.retry_condition and self.retry_condition.is_retry_required(resp):
            resp = self.handle_request(path, method, data, headers)

        # Handling errors
        resp = resp if not self.error_handler else self.error_handler.handle_error(resp, req)

        return resp
