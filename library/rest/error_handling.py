class ErrorHandler():
    """Provides an abstraction for handling errors when consuming REST API services."""

    def handle_error(self, response, request, client):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        if response.status_code >= 400:
            raise Exception('Request "{} {}" failed!'.format(request.method, request.path))
