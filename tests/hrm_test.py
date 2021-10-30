import random
import time
import unittest
import bs4

from requests import Session
from faker import Faker



class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://hrm-online.portnov.com/symfony/web/index.php"

        self.sess = Session()
        self.sess.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})

    def test_create_employee(self):
        #  Step 1: get the landing page - contains login form
        login_uri = "/auth/login"
        resp = self.sess.get(self.url + login_uri)

        # Step 2: extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})
        token = result['value']

        authenticate_uri = '/auth/validateCredentials'

        # Step 3: Login by posting credentials + CSRF token
        login_data = {
            '_csrf_token': token,
            'txtUsername': 'admin',
            'txtPassword': 'password'
        }
        resp = self.sess.post(self.url + authenticate_uri, data=login_data)

        self.assertIn('/pim/viewEmployeeList', resp.url)
        # OR
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        # Step 4: get the add employee page - contains the Form to add employee
        add_employee_uri = "/pim/addEmployee"
        resp = self.sess.get(self.url + add_employee_uri)

        # Step 5: extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': '_csrf_token'})['value']

        #  to select random
        emp_id = str(time.time()).split('.')[-1]
        #     or
        emp_id = random.randrange(100000,999999)
        #     or
        f = Faker()

        first_name = f.first_name()
        last_name = f.last_name()
        emp_id = f.random_number(6)

        emp_data = {
            "firstName": first_name,
            "lastName": last_name,
            "employeeId": emp_id,
            "_csrf_token": token
        }

        #  Step 6: add the employee - posting the new employee data + CSRF token
        resp = self.sess.post(self.url + add_employee_uri, data=emp_data)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        #  Optional: check that data posted correctly
        resp = self.sess.get(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']

        self.assertEqual(str(emp_id), actual_emp_id)




if __name__ == '__main__':
    unittest.main()
