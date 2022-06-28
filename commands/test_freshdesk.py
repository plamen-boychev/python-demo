from unittest import TestCase, mock
import json
import requests
from commands.freshdesk import ImportGitHubUserInFreshdesk

def mocked_requests_multiple_success(*args, **kwargs):
    """Mock requests to service."""

    # Fetching GitHub user details
    if 'GET' == args[0] and '/users/github_username' == args[1]:
        mock_response = mock.Mock(status_code=200)
        mock_response.content = json.dumps({
            "id": 1,
            "name": "test",
            "email": "test@corp.local",
            "login": "github_username",
            "repos_url": "example-url"
        }).encode('ascii')
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response
    # Updating Freshdesk contact details
    elif 'PUT' == args[0] and '/api/v2/contacts/1' == args[1]:
        mock_response = mock.Mock(status_code=200)
        mock_response.content = json.dumps({ "id": 1 }).encode('ascii')
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response
    # Creating a Freshdesk contact
    elif 'POST' == args[0] and '/api/v2/contacts' == args[1]:
        mock_response = mock.Mock(status_code=200)
        mock_response.content = json.dumps({ "id": 1 }).encode('ascii')
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response
    # Searching for a Freshdesk contact
    elif 'GET' == args[0] and '/api/v2/search/contacts?query="unique_external_id:github_username"' == args[1]:
        mock_response = mock.Mock(status_code=200)
        mock_response.content = json.dumps({ "results": [] }).encode('ascii')
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response

def mocked_requests_multiple_fail(*args, **kwargs):
    """Mock requests to service."""

    # Fetching GitHub user details
    if 'GET' == args[0] and '/users/github_username' == args[1]:
        mock_response = mock.Mock(status_code=404)
        mock_response.content = b""
        mock_response.headers = requests.structures.CaseInsensitiveDict()
        mock_response.headers['Content-Type'] = 'application/json'
        return mock_response

class TestCommand(TestCase):

    @mock.patch('requests.request', side_effect=mocked_requests_multiple_success)
    def test_e2e_process(self, request_mock):
        """Test happy path."""

        command = ImportGitHubUserInFreshdesk(
            github_username="github_username",
            freshdesk_subdomain="tests",
            github_token="github_token",
            freshdesk_token="freshdesk_token"
        )
        result = command.execute()
        self.assertEqual(result, True, "Importing contact should succeed!")

    @mock.patch('requests.request', side_effect=mocked_requests_multiple_fail)
    def test_e2e_process(self, request_mock):
        """Test API returns error."""

        command = ImportGitHubUserInFreshdesk(
            github_username="github_username",
            freshdesk_subdomain="tests",
            github_token="github_token",
            freshdesk_token="freshdesk_token"
        )
        self.assertRaises(Exception, command.execute)
