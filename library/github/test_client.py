from unittest import TestCase, mock
import time
import json
import requests
from library.github.githubclient import GitHubClient

class TestClient(TestCase):

    def test_delete_requests(self):
        """Test Basic authorization handler."""

    @mock.patch("requests.request")
    def test_ok_request(self, mock_post):
        """Test successful requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        response = client_obj.get("test")

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_bad_request(self, mock_post):
        """Test rate limit retry mechanism."""

        # TODO: Reduce the delay caused by retries

        my_mock_response = mock.Mock(status_code=403)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        my_mock_response.headers['X-RateLimit-Remaining'] = 0
        my_mock_response.headers['X-RateLimit-Reset'] = int(round(time.time())) + 1
        mock_post.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        """
        We're expecting the request to fail after a number of attempts
        since we're always providing 0 as remaining calls.
        """
        self.assertRaises(Exception, client_obj.get, "test")

    @mock.patch("requests.request")
    def test_fetching_user_details(self, mock_post):
        """Test fetching user details by username."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "login": "testuser" }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = GitHubClient(token="tokenval")
        response = client_obj.fet_user_details("testuser")
        """
        We're expecting the request to fail after a number of attempts
        since we're always providing 0 as remaining calls.
        """
        self.assertEqual(response.status_code, 200, "Fetching user details should return success status code!")
        self.assertEqual(response.headers["content-type"], "application/json", "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)["login"], "testuser", 'Mocked response should return expected "login" property value!')
