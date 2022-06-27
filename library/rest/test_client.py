from unittest import TestCase, mock
import json
import requests
from library.rest.client import Client

class TestClient(TestCase):

    base_path = "https://service.mock/api/v1"
    path = "/ping"

    @mock.patch("requests.request")
    def test_get_requests(self, mock_post):
        """Test GET requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = Client(self.base_path)
        response = client_obj.get(self.path)

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_post_requests(self, mock_post):
        """Test POST requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        headers = { "Accept": "application/json" }
        payload = { "test": True }
        base_path = "https://service.mock/api/v1"
        path = "/ping"

        client_obj = Client(base_path)
        response = client_obj.post(path, data=payload)

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_put_requests(self, mock_post):
        """Test PUT requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        headers = { "Accept": "application/json" }
        payload = { "test": True }
        base_path = "https://service.mock/api/v1"
        path = "/ping"

        client_obj = Client(base_path)
        response = client_obj.put(path, data=payload)

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_patch_requests(self, mock_post):
        """Test PATCH requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        headers = { "Accept": "application/json" }
        payload = { "test": True }
        base_path = "https://service.mock/api/v1"
        path = "/ping"

        client_obj = Client(base_path)
        response = client_obj.patch(path, data=payload)

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')

    @mock.patch("requests.request")
    def test_delete_requests(self, mock_post):
        """Test DELETE requests."""

        my_mock_response = mock.Mock(status_code=204)
        my_mock_response.content = json.dumps({ "pong": True }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        client_obj = Client(self.base_path)
        response = client_obj.delete(self.path)

        self.assertEqual(response.status_code, 204, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['pong'], True, 'Mocked response should return expected "pong" property value!')
