import json
import unittest

import bs4

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

        add_candidate = sess.post_new_candidate('ABCD', 'AB', 'email@bom.com', 'newPassw')

        json_parsed = json.loads(add_candidate.text)
        user_id = json_parsed['id']
        print(user_id)
        self.assertTrue(json_parsed['email'] == 'email@bom.com')
        self.assertTrue(json_parsed['firstName'] == 'ABCD')
        self.assertTrue(json_parsed['lastName'] == 'AB')

        candidates = sess.get_all_candidates()
        json_parsed = json.loads(candidates.text)

        self.assertGreater(len(json_parsed), count)

    def test_delete_candidate(self, user_id, token ):
        sess = Authenticate()

        delete_candidate = sess.delete_candidate(user_id, token)

        # # candidates = sess.get_all_candidates()
        json_parsed = json.loads(delete_candidate.text)
        #
        # # self.assertLess(len(json_parsed), count)
        self.assertFalse(json_parsed['email'] == 'email@bom.com')
        # self.assertFalse(json_parsed['firstName'] == 'ABCD')
        # self.assertFalse(json_parsed['lastName'] == 'AB')
        # self.assertFalse(json_parsed['id'] == 631)

if __name__ == '__main__':
    unittest.main()
