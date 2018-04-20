
"""
Customer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import os
import unittest
import logging
import json
import server
from flask_api import status
from models import Customer, DataValidationError
from mock import MagicMock, patch


######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    def setUp(self):
        self.app = server.app.test_client()
        server.initialize_logging(logging.CRITICAL)
        server.init_db()
        server.data_reset()
        server.data_load({"username":"MeenakshiSundaram", "password":"123", "firstname":"Meenakshi", "lastname":"Sundaram",
            "address":"Jersey City", "phone":"2016604601","email":"msa503@nyu.edu", "status":1, "promo":1})
        server.data_load({"username":"jf", "password":"12345", "firstname":"jinfan", "lastname":"yang",
            "address":"nyu", "phone":"123-456-7890","email":"jy2296@nyu.edu", "status":1, "promo":0})

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
#        data = json.loads(resp.data)
#        self.assertEqual(data['name'], 'Customer REST API Service')

    def test_get_customer_list(self):
        """ Get a list of Customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_customer_promo_list(self):
        """ Get a list of Customers with promo"""
        customer = Customer.find_by_promo(1)
        resp = self.app.get('/customers/promo/1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertTrue(len(data) > 0)

    def test_get_customer_by_username(self):
        """ Get customer by username """
        customer = Customer.find_by_username('jf')[0]
        resp = self.app.get('/customers?username=jf')
        data = json.loads(resp.data)
        self.assertEqual(data['username'], customer.username)
        self.assertEqual(data['id'], customer.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        customer = Customer.find_by_username('jf')[0]
        resp = self.app.get('/customers/{}'.format(customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['username'], customer.username)

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """ Create a new Customer """
        # save the current number of customers for later comparison
        customer_count = self.get_customer_count()

        # add a new customer
        new_customer = {"username": "ms",
                        "password": "11111",
                        "firstname": "mary",
                        "lastname": "sue",
                        "address": "nyu",
                        "phone": "123-456-7890",
                        "email": "marysue@gmail.com",
                        "status": 0,
                        "promo": 1}

        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)

        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['username'], 'ms')

        # check that count has gone up
        resp = self.app.get('/customers')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), customer_count + 1)
        self.assertIn(new_json, data)

    def test_update_customer(self):
        """ Update an existing Customer """
        customer = Customer.find_by_username('jf')[0]
        new_customer = {"username": "jf",
                        "password": "12345",
                        "firstname": "jinfan",
                        "lastname": "yang",
                        "address": "nyu",
                        "phone": "123-456-7890",
                        "email": "jy2296@nyu.edu",
                        "status": 0,
                        "promo": 1}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 0)

    def test_subscribe_customer(self):
        """ Subscribe an existing Customer"""
        customer = Customer.find_by_username('jf')[0]
        new_customer = {"username": customer.username,
                        "password": customer.password,
                        "firstname": customer.firstname,
                        "lastname": customer.lastname,
                        "address": customer.address,
                        "phone": customer.phone,
                        "email": customer.email,
                        "status": customer.status,
                        "promo": 1}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}/subscribe'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['promo'], 1)

    def test_deactivate_customer(self):
        """ Deactivate an existing Customer"""
        customer = Customer.find_by_username('jf')[0]
        new_customer = {"username": customer.username,
                        "password": customer.password,
                        "firstname": customer.firstname,
                        "lastname": customer.lastname,
                        "address": customer.address,
                        "phone": customer.phone,
                        "email": customer.email,
                        "status": 0,
                        "promo": customer.promo}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}/deactivate'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['status'], 0)

    def test_delete_customer(self):
        """ Delete a Customer """
        customer = Customer.find_by_username('jf')[0]

        # save the current number of pets for later comparrison
        customer_count = self.get_customer_count()
        resp = self.app.delete('/customers/{}'.format(customer.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_customer_count()
        self.assertEqual(new_count, customer_count - 1)

    def test_not_found_error(self):
        """ Test showing exception handling 404 """
        rv = self.app.get('/4444')
        self.assertEqual(rv.status_code, 404)

    def test_get_nonexisting_customer(self):
        """ Get a nonexisting Customer """
        resp = self.app.get('/customers/5')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_call_create_with_an_id(self):
        """ Call create passing an id """
        new_customer = {"username": "jk",
                        "password": "249",
                        "firstname": "jahn",
                        "lastname": "kalyani",
                        "address": "raleigh",
                        "phone": "632-262-6362",
                        "email": "jk1378@nyu.edu",
                        "status": 1,
                        "promo": 0}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers/1', data=data)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_bad_request(self):
        """ Test a Bad Request error from Update Customer """
        new_customer = {"useinvalidame": "jf"}
        data = json.dumps(new_customer)
        resp = self.app.put('/customers/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_exception_update_customer(self):
        """ Test not found exception error from update customer"""
        new_customer = {"username": "jf",
                        "password": "12345",
                        "firstname": "jinfan",
                        "lastname": "yang",
                        "address": "nyu",
                        "phone": "123-456-7890",
                        "email": "jy2296@nyu.edu",
                        "status": 0,
                        "promo": 1}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/1000000', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_found_get_customer_by_username(self):
        """ Test a Not Found error from Find By UserId """
        #not_found_mock.side_effect = server.HTTP_404_NOT_FOUND
        resp = self.app.get('/customers?username=IDONOTEXIST')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed_customer_email_search(self):
        """ Test a Method not Supported error from Customer Search """
        #not_found_mock.side_effect = server.HTTP_404_NOT_FOUND
        resp = self.app.get('/customers?email=amnot@right.com')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

######################################################################
# Utility functions
######################################################################

    def get_customer_count(self):
        """ save the current number of customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
