from unittest import TestCase, mock
import time
import json
import requests
from library.github.githubclient import GitHubClient

req_attempts = 0

def mocked_requests_multiple(*args, **kwargs):
    """Mock requests to service."""
    global req_attempts
    req_attempts += 1
    if 1 == req_attempts:
        mock_response = mock.Mock(status_code=403)
        mock_response.content = b""
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        mock_response.headers['X-RateLimit-Remaining'] = 0
        mock_response.headers['X-RateLimit-Reset'] = int(round(time.time())) + 0.1
        return mock_response
    else:
        mock_response = mock.Mock(status_code=200)
        mock_response.content = json.dumps({ "login": "testuser" }).encode('ascii')
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response

class TestClient(TestCase):

    @mock.patch("requests.request")
    def test_ok_request(self, request_mock):
        """Test successful requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        request_mock.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        response = client_obj.get("test")

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_bad_request(self, request_mock):
        """Test rate limit retry mechanism - error case."""

        my_mock_response = mock.Mock(status_code=403)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        my_mock_response.headers['X-RateLimit-Remaining'] = 0
        my_mock_response.headers['X-RateLimit-Reset'] = int(round(time.time())) + 1
        request_mock.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        """
        We're expecting the request to fail after a number of attempts
        since we're always providing 0 as remaining calls.
        """
        self.assertRaises(Exception, client_obj.get, "test")

    @mock.patch('requests.request', side_effect=mocked_requests_multiple)
    def test_retried_request(self, request_mock):
        """Test rate limit retry mechanism - happy path."""

        client_obj = GitHubClient(token="tokenval")
        response = client_obj.fetch_user_details("testuser")
        # First attemp should fail, then second should pass
        self.assertEqual(response.status_code, 200, "Fetching user details should return success status code!")
        self.assertEqual(response.headers["content-type"], "application/json", "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)["login"], "testuser", 'Mocked response should return expected "login" property value!')
        self.assertEqual(len(request_mock.call_args_list), 2, "Request needs to be successful on the second attempt!")

    @mock.patch("requests.request")
    def test_fetching_user_details(self, request_mock):
        """Test fetching user details by username."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "login": "testuser" }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        request_mock.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        response = client_obj.fetch_user_details("testuser")
        """
        We're expecting the request to fail after a number of attempts
        since we're always providing 0 as remaining calls.
        """
        self.assertEqual(response.status_code, 200, "Fetching user details should return success status code!")
        self.assertEqual(response.headers["content-type"], "application/json", "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)["login"], "testuser", 'Mocked response should return expected "login" property value!')
