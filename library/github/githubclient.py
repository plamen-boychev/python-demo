# TODO: Find a better way to import the library module
import sys
sys.path.insert(0, '../rest')

import time  
from auth import GenericAuth
from error_handling import ErrorHandler
from client import Client as BaseClient

class GitHubErrorHandler(ErrorHandler):
    """Handler for API errors for the GitHub REST API service."""

    # TODO: Make retries configurable
    max_retries = 5
    retries = 0

    # TODO: Avoid:
    #       - Passing the client as a parameter
    #       - Recusrion - possible stack overflow
    #       - Create a reusable rate limit mechanism for both GitHub and Freshdesk clients -
    #         the only difference is in the calculation of delay before next attempt
    def handle_error(self, response, request, client):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        if response.status_code > 299 and "X-RateLimit-Remaining" in response.headers and "X-RateLimit-Reset" in response.headers and 0 == response.headers["X-RateLimit-Remaining"]:
            if self.retries > self.max_retries:
                raise Exception("Too many unsuccessful attempts to execute the request!")
            now = int(round(time.time()))
            retry_after = response.headers["X-RateLimit-Reset"] - now
            print("Rate limit exceeded. Will retry in {} seconds".format(retry_after))
            time.sleep(retry_after)
            self.retries += 1
            client.execute_request(request)
        return response

class GitHubClient(BaseClient):
    """A GitHub service client class definition.
    Handles REST API communication."""

    def __init__(self, base_path=None, headers=None, auth=None, error_handler=None, credentials=None):
        """Initializing a client."""
        base_path = base_path if base_path else "https://api.github.com"
        headers = headers if headers else {}
        headers["Accept"] = "application/vnd.github.v3+json"
        # TODO: Verify credentials are valid
        auth = auth if auth else GenericAuth(credentials, "token")
        error_handler = error_handler if error_handler else GitHubErrorHandler()
        super().__init__(base_path, headers, auth, error_handler)

    def fet_user_details(self, user_login):
        """Enables fetchid a user details by its username / login."""
        # TODO: Validate input
        return self.get("/users/{}".format(user_login));
