import time
from library.rest.auth import Auth, BasicAuth
from library.rest.error_handling import ErrorHandler
from library.rest.client import Client as BaseClient, RetryCondition
from library.rest.request import Request
from library.rest.response import Response

class FreshdeskClient(BaseClient):
    """A Freshdesk service client class definition.
    Handles REST API communication."""

    def __init__(self, subdomain:str=None, api_key:str=None, headers:dict=None, auth:Auth=None, error_handler:ErrorHandler=None):
        """Initializing a client."""
        # TODO: Validate subdomain
        base_path = "https://{}.freshdesk.com".format(subdomain)
        headers = headers if headers else {}
        # TODO: Verify credentials are valid
        # Password is a required parameter, but not really used, so we're
        # providing a placeholder, as per the official documentation.
        credentials = {
            "user": api_key,
            "password": "X"
        }
        auth = auth if auth else BasicAuth(credentials)
        super().__init__(base_path, headers, auth, error_handler, FreshdeskRetryCondition())

    def persist_contact(self, user_login:str, details:dict):
        """Enables fetching a user details by its username / login."""
        # TODO: Validate input
        path = '/api/v2/search/contacts?query="unique_external_id:{}"'.format(user_login)
        existing_contacts = self.get(path).get_json(True)
        if len(existing_contacts["results"]):
            contact = existing_contacts["results"][0]
            return self.put("/api/v2/contacts/{}".format(contact.id), contact | details);
        else:
            return self.post("/api/v2/contacts", details);

class FreshdeskRetryCondition(RetryCondition):
    """Detects retry errors for the Freshdesk REST API service, indicates retry is required."""

    # TODO: Make retries configurable
    max_retries = 5
    retries = 0

    def is_retry_required(self, response:Response):
        """Detects an error in the response. If would not raise an exception should return a response object"""
        if response.status_code >= 400 and "X-RateLimit-Remaining" in response.headers and "Retry-After" in response.headers and 0 == response.headers["X-RateLimit-Remaining"]:
            if self.retries > self.max_retries:
                raise Exception("Too many unsuccessful attempts to execute the request!")
            now = int(round(time.time()))
            retry_after = response.headers["Retry-After"]
            # TODO: Log details in a proper way - should not be visible when running tests
            # print("Rate limit exceeded. Will retry in {} seconds".format(retry_after))
            time.sleep(retry_after)
            self.retries += 1
            return True
        return False
