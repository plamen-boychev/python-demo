from unittest import TestCase, mock
import json
import requests
from library.rest.request import HTTPVerb, Request

class TestRequest(TestCase):

    def test_empty_constructor(self):
        """Test correct behavior on no parameters provided in constructor."""

        request_object = Request(headers={})
        self.assertEqual(request_object.headers, { "Content-Type": "application/json" }, "Headers should be an empty dictionary!")
        self.assertEqual(request_object.payload, None, "Status code should be None!")
        self.assertEqual(request_object.method, None, "Status code should be None!")
        self.assertEqual(request_object.path, None, "Status code should be None!")

    def test_parameters_checks(self):
        """Test bad parameter values detection."""

        request_object = Request()
        self.assertRaises(Exception, request_object.set_headers, [])
        self.assertRaises(Exception, request_object.set_method, "passing string")
        self.assertRaises(Exception, request_object.set_method, 1)
        self.assertRaises(Exception, request_object.set_path, 1)

    def test_valid_params_are_ok(self):
        """Test valid parameters are accepted with no problems."""

        headers = { "Accept": "application:json" }
        payload = { "test": True }
        method = HTTPVerb.post
        path = "/api/vN/resourceName"

        # Check constructor
        request_object = Request(method, path, payload, headers)
        self.assertEqual(request_object.headers, { "Content-Type": "application/json", "Accept": "application:json" }, "Headers should be decorated with content type!")
        self.assertEqual(request_object.payload, payload, "Payload should be available as injected!")
        self.assertEqual(request_object.method, method, "Method should be available as injected!")
        self.assertEqual(request_object.path, path, "Path should be available as injected!")

        # Check setters
        new_request = Request()
        new_request.set_headers(headers)
        new_request.set_payload(payload)
        new_request.set_method(method)
        new_request.set_path(path)
        self.assertEqual(new_request.headers, { "Content-Type": "application/json", "Accept": "application:json" }, "Headers should be decorated with content type!")
        self.assertEqual(new_request.payload, payload, "Payload should be available as injected!")
        self.assertEqual(new_request.method, method, "Method should be available as injected!")
        self.assertEqual(new_request.path, path, "Path should be available as injected!")

    @mock.patch("requests.request")
    def test_invoke_requests(self, mock_post):
        """Test invoking requests."""

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = json.dumps({
            "login": "defunkt",
            "id": 2,
            "node_id": "MDQ6VXNlcjI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/defunkt",
            "html_url": "https://github.com/defunkt",
            "followers_url": "https://api.github.com/users/defunkt/followers",
            "following_url": "https://api.github.com/users/defunkt/following{/other_user}",
            "gists_url": "https://api.github.com/users/defunkt/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/defunkt/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/defunkt/subscriptions",
            "organizations_url": "https://api.github.com/users/defunkt/orgs",
            "repos_url": "https://api.github.com/users/defunkt/repos",
            "events_url": "https://api.github.com/users/defunkt/events{/privacy}",
            "received_events_url": "https://api.github.com/users/defunkt/received_events",
            "type": "User",
            "site_admin": False,
            "name": "Chris Wanstrath",
            "company": None,
            "blog": "http://chriswanstrath.com/",
            "location": None,
            "email": None,
            "hireable": None,
            "bio": "🍔",
            "twitter_username": None,
            "public_repos": 107,
            "public_gists": 273,
            "followers": 21451,
            "following": 210,
            "created_at": "2007-10-20T05:24:19Z",
            "updated_at": "2022-06-01T23:46:26Z"
        }).encode('ascii')
        my_mock_response.headers = requests.structures.CaseInsensitiveDict()
        my_mock_response.headers['Content-Type'] = 'application/json'
        mock_post.return_value = my_mock_response

        headers = { "Accept": "application/json" }
        payload = { "test": True }
        method = HTTPVerb.get
        path = "https://api.github.mock/users/defunkt"

        # Check constructor
        request_object = Request(method, path, payload, headers)
        response = request_object.invoke_request()

        self.assertEqual(response.status_code, 200, "Mocked response should return expected status code!")
        self.assertEqual(response.headers['content-type'], 'application/json', "Mocked response should return expected content type header!")
        self.assertEqual(response.get_json(True)['login'], 'defunkt', 'Mocked response should return expected "login" property value!')
