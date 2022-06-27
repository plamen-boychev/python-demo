from unittest import TestCase, mock
import requests
from library.rest.client import Client
from library.rest.error_handling import ErrorHandler

class ErrorRaiser(ErrorHandler):
    """Extends the abstract error handler. Provides means of testing the integration with the Client class."""

    def handle_error(self, response, request, client):
        """Raises an exception in case of a non 200 response code."""
        if 200 != response.status_code:
            raise Exception("API error response detected!")

class ErrorDampener(ErrorHandler):
    """Extends the abstract error handler. Provides means of testing the integration with the Client class."""

    def handle_error(self, response, request, client):
        """Changes the status code in case of a non 200 response code."""
        if 200 != response.status_code:
            response.set_status_code(200)
        return response

class TestAuth(TestCase):

    @mock.patch("requests.request")
    def test_get_requests(self, mock_post):
        """Test error handling."""

        my_mock_response = mock.Mock(status_code=404)
        my_mock_response.content = b""
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = client.Client("https://example.service.local/api/v1", error_handler=ErrorRaiser())

        self.assertRaises(Exception, client_obj.get, "/resource")

    @mock.patch("requests.request")
    def test_get_requests(self, mock_post):
        """Test error handling."""

        my_mock_response = mock.Mock(status_code=404)
        my_mock_response.content = b""
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = Client("https://example.service.local/api/v1", error_handler=ErrorDampener())
        res = client_obj.get("/resource")

        self.assertEqual(res.status_code, 200, "Error handler should be able to modify or replace a response with error!")
