import json
import unittest

import requests


class YahoAPITestCase(unittest.TestCase):
    def test_for_successful_response(self):
        result = requests.get("https://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # or
        self.assertTrue('OK' == result.reason)


class CareerPortalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

    def test_login(self):
        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']
        self.assertTrue(token)

        # verify_header = self.headers
        # verify_header['Authorization'] = 'Bearer' + token
        # or
        verify_header = {'Authorization': 'Bearer ' + token}
        verify_header.update(self.headers)

        verify_response = requests.post(self.base_url + '/verify', headers=verify_header)
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        user_email = verify_content["email"]
        user_first_name = verify_content["firstName"]
        user_last_name = verify_content["lastName"]
        user_address = verify_content["address"]

        self.assertEqual(8, user_id)
        self.assertTrue(user_email == 'student@example.com')
        self.assertEqual('Student', user_first_name)
        self.assertTrue(user_last_name == '')
        self.assertTrue(user_address == '4970 El Camino Real')

        positions = requests.get(self.base_url + '/positions')
        json_positions = json.loads(positions.text)

        self.assertGreaterEqual(len(json_positions), 5)

        my_positions = requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions')
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(len(json_my_positions), 6)


if __name__ == '__main__':
    unittest.main()
