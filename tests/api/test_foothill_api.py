import json
import unittest

import requests


class FoothillApiTests(unittest.TestCase):
    def get_foothill_course_search(self):
        return requests.get(url='https://catalog.foothill.edu/course-search/')

    def post_foothill_course_search(self, keyword=None, page=None, route=None, payload=None, **params):
        default_params = {
            'page': page or 'fose',
            'route': route or 'search',
            'keyword': keyword
        }
        hearders ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'Content-Type': 'application/json'
        }
        json = {
            "other": {"srcdb": ""},
            "criteria": [
                {"field": "keyword", "value": keyword}]}

        params = params if params is not None else default_params
        data = payload if payload is not None else json

        return requests.post(url='https://catalog.foothill.edu/course-search/api/', params=params, headers=hearders, json=data)


    def test_foothill_catalog_api(self):
        response = self.get_foothill_course_search()
        self.assertEqual(200, response.status_code)
        self.assertIn("course-search", response.url)

        self.assertIn('COURSE SEARCH', response.text)



    def test_search_course_catalogue(self):
        response = self.post_foothill_course_search('math')
        search_results = json.loads(response.text).get('results')
        # for i in search_results:
        #     if i.get('code') == "MATH 180":
        #         break
        # else:
        #     # self.fail('MATH 180 not found')
        # #     or
        #    assert False, "MATH 180 not found"

        # # or
        # found = False
        # for i in search_results:
        #     if i.get('code') == "MATH 180":
        #         found = True
        # self.assertTrue(found, "MATH 180 not found")
        #
        #or
        classes = list(x.get('code') for x in search_results)
        self.assertIn("MATH 180", classes)
        self.assertIn("MATH 10", classes)
        #to find several keys:
        classes = list({x.get('code'):x.get('title')} for x in search_results)
        self.assertIn({'MATH 180': 'QUANTITATIVE REASONING'}, classes)
        self.assertIn({'MATH 10': 'ELEMENTARY STATISTICS'}, classes)

    def test_search_no_keyword(self):
        response = self.post_foothill_course_search()
        self.assertEqual('{"fatal":"criterion.value is null"}', response.text)

    def test_search_bad_route(self):
        response = self.post_foothill_course_search(keyword='art', route='BAD')
        self.assertEqual('{"fatal":"Unknown route \\"BAD\\""}', response.text)

    def test_search_empty_page(self):
        response = self.post_foothill_course_search(keyword='art', page=' ')
        self.assertEqual('', response.text)

    def test_search_bad_payload(self):
        payload = {}
        response = self.post_foothill_course_search(keyword='art', payload=payload)
        self.assertEqual('{"fatal":"searchData.other is undefined"}', response.text)

    def test_search_partial_payload(self):
        keyword = 'art'
        payload = {
            "other": {"srcdb": ""},
            "criteria": [
                {"field": "keyword", "value": keyword}]}
        response = self.post_foothill_course_search(keyword='art', payload=payload)
        self.assertEqual('', response.text)



    def test_search_bad_params(self):
        response = self.post_foothill_course_search(fruit='kiwi', boy='male')
        self.assertEqual('', response.text)




if __name__ == '__main__':
    unittest.main()
