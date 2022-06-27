from unittest import TestCase
from library.rest.auth import BasicAuth
from library.rest.request import Request

from base64 import b64decode

class TestAuth(TestCase):

    def test_delete_requests(self):
        """Test Basic authorization handler."""

        creds = {
            "user": "myuser",
            "password": "mypass"
        }
        scheme = "Basic"

        req = Request()
        basic = BasicAuth(creds, scheme)
        req = basic.decorate_request(req)
        auth_header = req.headers["Authorization"]
        header_extract = b64decode(auth_header.replace("{} ".format(scheme), "")).decode("ascii").split(":")

        self.assertTrue(auth_header.startswith(scheme), "Auth scheme is not available in the authorization header!")
        self.assertEqual(header_extract[0], creds["user"], "User value is not available in the authorization header!")
        self.assertEqual(header_extract[1], creds["password"], "Password value is not available in the authorization header!")
