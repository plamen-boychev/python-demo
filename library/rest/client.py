from library.rest.request import Request, HTTPVerb
from library.rest.auth import Auth
from library.rest.error_handling import ErrorHandler

class Client:
    """A base service client class definition.
    Handles communication with a service."""

    base_path = None
    headers = None
    auth = None
    error_handler = None

    def __init__(self, base_path, headers=None, auth=None, error_handler=None):
        """Initializing a client."""
        if auth and False == isinstance(auth, Auth):
            raise Exception("Authorization handler needs to be an implementation of Auth class, {} provided".format(type(auth)))
        if error_handler and False == isinstance(error_handler, ErrorHandler):
            raise Exception("Error handler needs to be an implementation of ErrorHandler class, {} provided".format(type(auth)))

        self.base_path = base_path
        self.headers = headers if headers else None
        self.auth = auth if auth else None
        self.error_handler = error_handler if error_handler else None

    def get(self, path, headers=None):
        """Execute GET requests."""
        return self.handle_request(path, HTTPVerb.get, headers=headers);

    def post(self, path, data, headers=None):
        """Execute POST requests."""
        return self.handle_request(path, HTTPVerb.post, data=data, headers=headers);

    def put(self, path, data, headers=None):
        """Execute PUT requests."""
        return self.handle_request(path, HTTPVerb.put, data=data, headers=headers);

    def patch(self, path, data, headers=None):
        """Execute PATCH requests."""
        return self.handle_request(path, HTTPVerb.patch, data=data, headers=headers);

    def delete(self, path, headers=None):
        """Execute DELETE requests."""
        return self.handle_request(path, HTTPVerb.delete, headers=headers);

    def build_request(self, path, method, data=None, headers=None):
        """Creating request objects."""
        full_path = self.base_path + path
        return Request(method, path, data, headers)

    def handle_request(self, path, method, data=None, headers=None):
        """Executing a previously built request object."""
        req = self.build_request(path, HTTPVerb.delete, headers=headers);
        if self.auth:
            self.auth.decorate_request(req)
        return self.execute_request(req)
    
    def execute_request(self, request):
        resp = request.invoke_request()
        return resp if not self.error_handler else self.error_handler.handle_error(resp, request, self)
