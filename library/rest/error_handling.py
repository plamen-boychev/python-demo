from abc import ABC, abstractmethod

class ErrorHandler(ABC):
    """Provides an abstraction for handling errors when consuming REST API services."""

    @abstractmethod
    def handle_error(self, response, request, client):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        pass
