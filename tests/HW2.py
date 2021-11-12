import json
import unittest

from lib.authentication import Authenticate


class TestCase(unittest.TestCase):
    def test_add_candidate(self):
        sess = Authenticate()

        candidates = sess.get_all_candidates()
        json_parsed = json.loads(candidates.text)

        count = 0
        for el in json_parsed:
            count += 1

        print(count)
        print(len(json_parsed))
        self.assertEqual(len(json_parsed), count)

        add_candidate = sess.post_new_candidate('ABCD', 'AB', 'email@boms.com', 'newPassw')

        json_parsed = json.loads(add_candidate.text)
        user_id = json_parsed.get('id')
        print(user_id)
        self.assertTrue(json_parsed['email'] == 'email@boms.com')
        self.assertTrue(json_parsed['firstName'] == 'ABCD')
        self.assertTrue(json_parsed['lastName'] == 'AB')

        candidates = sess.get_all_candidates()
        json_parsed = json.loads(candidates.text)

        self.assertGreater(len(json_parsed), count)

    def test_login_as_new_candidate(self):
        sess = Authenticate()
        result = sess.authenticate('email@boms.com', 'newPassw')
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        result = sess.logout()
        self.assertEqual(200, result.status_code)
        json_parsed = json.loads(result.text)
        self.assertEqual({'authenticated': False, 'token': None}, json_parsed)

    def test_create_and_delete_candidate(self):
        sess = Authenticate()
        result = sess.authenticate('student@example.com', 'welcome')
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        candidates = sess.get_all_candidates()
        json_parsed = json.loads(candidates.text)

        count = 0
        for el in json_parsed:
            count += 1

        print(count)
        print(len(json_parsed))
        self.assertEqual(len(json_parsed), count)

        add_candidate = sess.post_new_candidate('ABCD', 'AB', 'email@bosss.com', 'newPassw')

        json_parsed = json.loads(add_candidate.text)
        user_id = json_parsed.get('id')
        print(user_id)
        self.assertTrue(json_parsed['email'] == 'email@bosss.com')
        self.assertTrue(json_parsed['firstName'] == 'ABCD')
        self.assertTrue(json_parsed['lastName'] == 'AB')



        delete_candidate = sess.delete_candidate(user_id)
        self.assertEqual(204, delete_candidate.status_code)


if __name__ == '__main__':
    unittest.main()
