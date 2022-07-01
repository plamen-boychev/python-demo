from library.rest.request import Request
from library.rest.response import Response

class ErrorHandler():
    """Provides an abstraction for handling errors when consuming REST API services."""

    def handle_error(self, response:Response, request:Request):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        if response.status_code >= 400:
            raise Exception('Request "{} {}" failed with status code {} and payload: {}'
                .format(request.method, request.path, response.status_code, response.payload))
        return response
