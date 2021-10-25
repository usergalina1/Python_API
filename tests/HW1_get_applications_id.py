import json
import unittest

import requests
from parameterized import parameterized


class CareerPortalTest(unittest.TestCase):
    options = [
        ('code_200', 1, 200, ''),
        ('code_400', 999, 400, 'errorMessage":"Incorrect applicationId: 999'),
        ('code_500', "one", 500, 'ER_BAD_FIELD_ERROR')
    ]

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

    @parameterized.expand(options)
    def test_get_applications_id(self, test_name, application_id, status_code, error_message):
        applications = self.get_applications_id(application_id)
        self.assertEqual(status_code, applications.status_code)

    def get_applications_id(self, application_id):
        return requests.get(self.base_url + '/applications/' + str(application_id))
