import json

import requests


class Authenticate(object):
    def __init__(self):
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})

    def get_all_positions(self):
        return self.session.get(self.base_url + '/positions')

    def authenticate(self, email, password):
        resp = self.session.post(self.base_url + '/login', json={"email": email, "password": password})
        json_parsed = json.loads(resp.text)
        token = json_parsed.get('token', False)
        if token:
            self.session.headers.update({'Authorization': 'Bearer ' + token})
        return resp

    def perform_user_verification(self):
        return self.session.post(self.base_url + '/verify')

    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

    def get_all_candidates(self):
        return self.session.get(self.base_url + '/candidates')

    def verify_candidate(self, user_id):
        return self.session.get(self.base_url + '/candidates' + str(user_id))

    def post_new_candidate(self, first_name, last_name, email, password):
        return self.session.post(self.base_url + '/candidates', json={
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password
        })

    def delete_candidate(self, user_id, token):
        token = self.session.headers.update({'Authorization': 'Bearer ' + token})
        return self.session.delete(self.base_url + '/candidates/' + str(user_id), headers=token)
