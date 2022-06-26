import request

class Client:
    """A base service client class definition.
    Handles communication with a service."""

    base_path = None
    headers = None

    def __init__(self, base_path, headers=None):
        """Initializing a client."""
        self.base_path = base_path
        self.headers = headers if headers else None

    def get(self, path, headers=None):
        """Execute GET requests."""
        return self.execute_request(self.build_request(path, request.HTTPVerb.get, headers=headers));

    def post(self, path, data, headers=None):
        """Execute POST requests."""
        return self.execute_request(self.build_request(path, request.HTTPVerb.post, data=data, headers=headers));

    def put(self, path, data, headers=None):
        """Execute PUT requests."""
        return self.execute_request(self.build_request(path, request.HTTPVerb.put, data=data, headers=headers));

    def patch(self, path, data, headers=None):
        """Execute PATCH requests."""
        return self.execute_request(self.build_request(path, request.HTTPVerb.patch, data=data, headers=headers));

    def delete(self, path, headers=None):
        """Execute DELETE requests."""
        return self.execute_request(self.build_request(path, request.HTTPVerb.delete, headers=headers));

    def build_request(self, path, method, data=None, headers=None):
        """Creating request objects."""
        full_path = self.base_path + path
        return request.Request(method, path, data, headers)

    def execute_request(self, request):
        """Executing a previously built request object."""
        return request.invoke_request()
