import time
from library.rest.auth import Auth, TokenAuth
from library.rest.error_handling import ErrorHandler
from library.rest.client import Client as BaseClient, RetryCondition
from library.rest.request import Request
from library.rest.response import Response

class GitHubClient(BaseClient):
    """A GitHub service client class definition.
    Handles REST API communication."""

    def __init__(self, token:str=None, base_path:str=None, headers:dict=None, auth:Auth=None, error_handler:ErrorHandler=None):
        """Initializing a client."""
        base_path = base_path if base_path else "https://api.github.com"
        headers = headers if headers else {}
        headers["Accept"] = "application/vnd.github.v3+json"
        # TODO: Verify credentials are valid
        auth = auth if auth else TokenAuth(token)
        super().__init__(base_path, headers, auth, error_handler, GitHubRetryCondition())

    def fetch_user_details(self, user_login:str):
        """Enables fetching a user details by its username / login."""
        # TODO: Validate input
        return self.get("/users/{}".format(user_login));

class GitHubRetryCondition(RetryCondition):
    """Detects retry errors for the GitHub REST API service, indicates retry is required."""

    # TODO: Make retries configurable
    max_retries = 5
    retries = 0

    def is_retry_required(self, response: Response):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        if response.status_code >= 400 and "X-RateLimit-Remaining" in response.headers and "X-RateLimit-Reset" in response.headers and 0 == response.headers["X-RateLimit-Remaining"]:
            if self.retries > self.max_retries:
                raise Exception("Too many unsuccessful attempts to execute the request!")
            now = int(round(time.time()))
            retry_after = response.headers["X-RateLimit-Reset"] - now
            # TODO: Log details in a proper way - should not be visible when running tests
            # print("Rate limit exceeded. Will retry in {} seconds".format(retry_after))
            time.sleep(retry_after)
            self.retries += 1
            return True
        return False
