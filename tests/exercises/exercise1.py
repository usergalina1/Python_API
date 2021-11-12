import json
import unittest

from parameterized import parameterized
from requests import Session


class TestCaseRegresIn(unittest.TestCase):
    options_of_users = [
        ('list_users', 'api/users?page=2', 200, 'api/users', 'OK', 'total'),
        ('single_user', 'api/users/2', 200, 'api/users', 'OK', 'data'),
        ('user_not_found', 'api/users/23', 404, 'api/users', 'Not Found', '')
    ]
    login = [
        ('positive', "eve.holt@reqres.in", "cityslicka", 200, 'api/login', 'QpwL5tke4Pnpja7X4', 'token'),
        ('negative', 'peter@klaven', '', 400, 'api/login', 'Missing password', 'error')
    ]

    def setUp(self) -> None:
        self.url = "https://reqres.in/"

        self.sess = Session()
        self.sess.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})

    @parameterized.expand(options_of_users)
    def test_list_users(self, test_name, user_api, status_code, url, reason, parsed_text):
        user_api = user_api
        response = self.sess.get(self.url + str(user_api))
        self.assertEqual(status_code, response.status_code)
        self.assertIn(url, response.url)
        self.assertIn(reason, response.reason)

        # json_parsed = json.loads(response.text)
        # self.assertTrue(json_parsed[parsed_text])

    def test_get_list_users(self):
        list_users = 'api/users?page=2'
        response = self.sess.get(self.url + list_users)
        self.assertEqual(200, response.status_code)
        self.assertEqual('https://reqres.in/api/users?page=2', response.url)
        self.assertIn('api/users', response.url)
        self.assertIn('OK', response.reason)

        json_parsed = json.loads(response.text)
        self.assertTrue(json_parsed['total'])
        self.assertEqual(6, len(json_parsed))

    def test_get_single_user(self):
        single_user = 'api/users/2'
        resp = self.sess.get(self.url + single_user)
        self.assertEqual(200, resp.status_code)
        self.assertTrue('ok')
        self.assertIn('api/users/2', resp.url)

        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['data'])

    def test_single_user_not_found(self):
        single_user = 'api/users/23'
        resp = self.sess.get(self.url + single_user)
        self.assertEqual(404, resp.status_code)
        self.assertEqual('Not Found', resp.reason)
        self.assertIn('api/users/23', resp.url)
        # json_parsed = json.loads(resp.text)
        # self.assertTrue(json_parsed[{}])
        self.assertEqual('{}', resp.text)

    def test_get_list_resource(self):
        list_resource = 'api/unknown'
        resp = self.sess.get(self.url + list_resource)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('OK', resp.reason)
        self.assertIn('api/unknown', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['data'])

    def test_get_single_resource(self):
        single_resource = 'api/unknown/2'
        resp = self.sess.get(self.url + single_resource)
        self.assertEqual(200, resp.status_code)
        self.assertTrue('ok')
        self.assertIn('api/unknown/2', resp.url)

        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['data'])

    def test_single_resource_not_found(self):
        single_user = 'api/unknown/23'
        resp = self.sess.get(self.url + single_user)
        self.assertEqual(404, resp.status_code)
        self.assertEqual('Not Found', resp.reason)
        self.assertIn('api/unknown/23', resp.url)
        self.assertEqual('{}', resp.text)

    def test_create_users(self):
        create_users = 'api/users'
        resp = self.sess.post(self.url + create_users, json={"name": "morpheus", "job": "leader"})
        self.assertEqual(201, resp.status_code)
        self.assertEqual('Created', resp.reason)
        self.assertIn('api/users', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['createdAt'])
        self.assertEqual('morpheus', json_parsed['name'])
        self.assertEqual('leader', json_parsed['job'])

    def test_update_users(self):
        update_users = 'api/users/2'
        resp = self.sess.put(self.url + update_users, json={"name": "morpheus", "job": "zion resident"})
        self.assertEqual(200, resp.status_code)
        self.assertEqual('OK', resp.reason)
        self.assertIn('api/users/2', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['updatedAt'])
        self.assertEqual('zion resident', json_parsed['job'])

    def test_update_users_with_patch(self):
        update_users = 'api/users/2'
        resp = self.sess.patch(self.url + update_users)
        self.assertEqual(200, resp.status_code)
        self.assertEqual('OK', resp.reason)
        self.assertIn('api/users/2', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['updatedAt'])

    def test_delete_users(self):
        delete_users = 'api/users/2'
        resp = self.sess.delete(self.url + delete_users)
        self.assertEqual(204, resp.status_code)
        self.assertEqual('No Content', resp.reason)
        self.assertIn('api/users/2', resp.url)
        self.assertEqual('', resp.text)

    def test_register(self):
        register_users = 'api/register'
        resp = self.sess.post(self.url + register_users, json={"email": "eve.holt@reqres.in", "password": "pistol"})
        self.assertEqual(200, resp.status_code)
        self.assertEqual('OK', resp.reason)
        self.assertIn('api/register', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertEqual(4, json_parsed['id'])
        self.assertEqual('QpwL5tke4Pnpja7X4', json_parsed['token'])

    def test_register_negative(self):
        register_users = 'api/register'
        resp = self.sess.post(self.url + register_users, json={"email": "sydney@fife"})
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Bad Request', resp.reason)
        self.assertIn('api/register', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertEqual('Missing password', json_parsed['error'])

    @parameterized.expand(login)
    def test_login(self, test_name, email, password, status_code, url, text, token):
        login = 'api/login'
        resp = self.sess.post(self.url + login, json={"email": email, "password": password})
        self.assertEqual(status_code, resp.status_code)
        self.assertIn(url, resp.url)
        json_parsed = json.loads(resp.text)
        self.assertEqual(text, json_parsed[token])

    def test_delay(self):
        delay = 'api/users?delay=3'
        resp = self.sess.get(self.url + delay)
        self.assertEqual(200, resp.status_code)
        self.assertIn('delay', resp.url)
        json_parsed = json.loads(resp.text)
        self.assertTrue(json_parsed['total'])


if __name__ == '__main__':
    unittest.main()
