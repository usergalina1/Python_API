import json as JSON

import requests


class RecruitApi:
    post_headers = {
        "Content-Type": "application/json"
    }

    def __init__(self):
        self.session = requests.Session()

    def login(self, email='student@example.com', password='welcome'):
        json = {
            "email": email,
            "password": password
        }

        result = self.session.post(
            url='https://recruit-portnov.herokuapp.com/recruit/api/v1/login',
            headers=self.post_headers,
            json=json
        )

        token: str = JSON.loads(result.text).get('token')
        self.session.headers = {'authorization': f'Bearer {token}'}

    def post_positions(self, title='', **kwargs):
        json = {
            "title": title,
            "address": kwargs.get('address'),
            "city": kwargs.get('city'),
            "state": kwargs.get('state'),
            "zip": kwargs.get('zip'),
            "description": kwargs.get('description'),
            "dateOpen": kwargs.get('dateOpen'),
            "company": kwargs.get('company')
        }

        return self.session.post(url="https://recruit-portnov.herokuapp.com/recruit/api/v1/positions",
                                 headers=self.post_headers,
                                 json=json
                                 )


api = RecruitApi()
api.login()
result = api.post_positions('API SDET GURU')
pass
