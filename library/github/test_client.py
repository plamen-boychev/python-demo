from unittest import TestCase, mock
import time
import json
import requests
import githubclient

class TestClient(TestCase):

    def test_delete_requests(self):
        """Test Basic authorization handler."""

    @mock.patch("request.requests.request")
    def test_ok_request(self, mock_post):
        """Test successful requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        creds = {
            "user": "myuser",
            "password": "mypass",
        }
        client_obj = githubclient.GitHubClient(credentials=creds)
        response = client_obj.get("test")

        print("response obj in tests: ", response)
        print("response obj in tests: ", response.status_code)

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("request.requests.request")
    def test_ok_request(self, mock_post):
        """Test successful requests."""

        my_mock_response = mock.Mock(status_code=403)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        my_mock_response.headers['X-RateLimit-Remaining'] = 0
        my_mock_response.headers['X-RateLimit-Reset'] = int(round(time.time())) + 1
        mock_post.return_value = my_mock_response

        creds = {
            "user": "myuser",
            "password": "mypass",
        }
        client_obj = githubclient.GitHubClient(credentials=creds)
        """
        We're expecting the request to fail after a number of attempts
        since we're always providing 0 as remaining calls.
        """
        self.assertRaises(Exception, client_obj.get, "test")
