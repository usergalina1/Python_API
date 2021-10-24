import json
import unittest

import requests
from parameterized import parameterized


class MyPositionsTest(unittest.TestCase):
    alist = [
        # ('user does not exist', 9999, 204, ''),
        ('letters', 'abc', 500, 'ER_BAD_FIELD_ERROR'),
        # ('space', ' ', 204, '')
    ]

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        self.authorization_header = {'Authorization': 'Bearer ' + token}
        self.authorization_header.update(self.headers)

    @parameterized.expand(alist)
    def test_get_candidate_positions(self, test_name, user_id, status_code, error_message):
        my_positions = requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions', headers=self.authorization_header)
        self.assertEqual(status_code, my_positions.status_code)

        json_my_positions = json.loads(my_positions.text)

        if json_my_positions:
            self.assertEqual(json_my_positions['code'], error_message)


if __name__ == '__main__':
    unittest.main()
