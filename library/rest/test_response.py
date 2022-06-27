import unittest
import json
import requests
from library.rest.response import Response

class TestResponse(unittest.TestCase):

    def test_empty_constructor(self):
        """Test correct behavior on no parameters provided in constructor."""
        response_object = Response()
        self.assertEqual(response_object.status_code, None, "Status code should be None!")
        self.assertEqual(response_object.headers, None, "Headers should be None!")
        self.assertEqual(response_object.payload, None, "Payload should be None!")

    def test_parameters_checks(self):
        """Test bad parameter values detection."""
        response_object = Response()
        self.assertRaises(Exception, response_object.set_status_code, "passing string")
        self.assertRaises(Exception, response_object.set_status_code, -1)
        self.assertRaises(Exception, response_object.set_headers, None)

    def test_parsing_payload(self):
        """Test parsing payload."""
        response_object = Response()

        # Setting a payload value - default behaviour
        response_object.set_payload('{"test":true}')
        self.assertEqual(response_object.get_json(), { "test" : True }, "Payload string should be parsed by default!")

        # Setting a payload value and NOT parsing it
        response_object.set_payload('{"test":false}', False)
        self.assertEqual(response_object.get_json(), { "test" : True }, "Payload string should not be parsed when explicitly specifying not to!")

        # Parsing the payload data explicitly when calling getter
        self.assertEqual(response_object.get_json(refresh=True), { "test" : False }, "Payload string should be parsed when explicitly specified to!")

        # Check parsing bad value raises an error
        # 1. When parsing the payload at the time it's being provided injected
        self.assertRaises(json.decoder.JSONDecodeError, response_object.set_payload, "{asd:asd}")
        # 2. When parsing the payload at the time it's being read as JSON property
        response_object.set_payload("{asd:asd}", parse=False)
        self.assertRaises(json.decoder.JSONDecodeError, response_object.get_json, True)

    def test_valid_params_are_ok(self):
        """Test valid parameters are accepted with no problems."""
        response_object = Response()

        # Setting a payload value - default behaviour
        response_object.set_payload('{"test":true}')
        self.assertEqual(response_object.get_json(), { "test" : True }, "Payload string should be parsed by default!")

        # Setting a payload value and NOT parsing it
        response_object.set_payload('{"test":false}', False)
        self.assertEqual(response_object.get_json(), { "test" : True }, "Payload string should not be parsed when explicitly specifying not to!")

        # Parsing the payload data explicitly when calling getter
        self.assertEqual(response_object.get_json(refresh=True), { "test" : False }, "Payload string should be parsed when explicitly specified to!")
