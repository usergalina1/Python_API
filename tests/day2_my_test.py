import json
import unittest

from lib_end_points.authenticate import Authenticate


class CareerPortalTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_login(self):
        sess = Authenticate()
        positions = sess.get_positions()
        json_positions = json.loads(positions.text)

        self.assertGreaterEqual(len(json_positions), 5)

        result = sess.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        verify_response = sess.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        user_email = verify_content["email"]

        self.assertEqual(8, user_id)
        self.assertTrue(user_email == 'student@example.com')

        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(6, len(json_my_positions))

    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
