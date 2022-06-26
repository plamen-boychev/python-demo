# TODO: Find a better way to import the library module
import sys
sys.path.insert(0, '../rest')

import time  
from auth import GenericAuth
from error_handling import ErrorHandler
from client import Client as BaseClient

class FreshdeskErrorHandler(ErrorHandler):
    """Handler for API errors for the Freshdesk REST API service."""

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
        if response.status_code > 299 and "X-RateLimit-Remaining" in response.headers and "Retry-After" in response.headers and 0 == response.headers["X-RateLimit-Remaining"]:
            if self.retries > self.max_retries:
                raise Exception("Too many unsuccessful attempts to execute the request!")
            now = int(round(time.time()))
            retry_after = response.headers["Retry-After"]
            print("Rate limit exceeded. Will retry in {} seconds".format(retry_after))
            time.sleep(retry_after)
            self.retries += 1
            client.execute_request(request)
        return response

class FreshdeskClient(BaseClient):
    """A Freshdesk service client class definition.
    Handles REST API communication."""

    def __init__(self, subdomain=None, api_key=None, headers=None, auth=None, error_handler=None):
        """Initializing a client."""
        # TODO: Validate subdomain
        base_path = "https://{}.freshdesk.com/api/v2/contacts".format(subdomain)
        headers = headers if headers else {}
        # TODO: Verify credentials are valid
        # Password is a required parameter, but not really used, so we're
        # providing a placeholder, as per the official documentation.
        credentials = {
            "user": api_key,
            "password": "X"
        }
        auth = auth if auth else GenericAuth(credentials, "Basic")
        error_handler = error_handler if error_handler else FreshdeskErrorHandler()
        super().__init__(base_path, headers, auth, error_handler)

    def persist_contact(self, user_login, details):
        """Enables fetchid a user details by its username / login."""
        # TODO: Validate input
        existing_contacts = self.get('/api/v2/search/contacts?query="unique_external_id:{}"'.format(user_login))
        if len(existing_contacts["results"]):
            contact = existing_contacts["results"][0]
            return self.put("/api/v2/contacts/{}".format(contact.id), contact | details);
        else:
            return self.post("/api/v2/contacts", details);
