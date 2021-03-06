
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
from app import server
from flask_api import status
from app.models import Customer
from app.custom_exceptions import DataValidationError
from mock import MagicMock, patch


######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Test Cases for Customer Server """

    def setUp(self):
        self.app = server.app.test_client()
        server.initialize_logging(logging.CRITICAL)
        server.init_db()
        server.data_reset()
        server.data_load({"username":"MeenakshiSundaram", "password":"123", "firstname":"Meenakshi", "lastname":"Sundaram",
            "address":"Jersey City", "phone":"2016604601","email":"msa503@nyu.edu", "active":True, "promo":True})
        server.data_load({"username":"jf", "password":"12345", "firstname":"jinfan", "lastname":"yang",
            "address":"nyu", "phone":"123-456-7890","email":"jy2296@nyu.edu", "active":True, "promo":False})
        server.data_load({"username":"jfy2", "password":"1234567", "firstname":"jinfan", "lastname":"yang",
            "address":"eastvillage", "phone":"123-456-7890","email":"jfy@nyu.edu", "active":True, "promo":False})


    def test_healthcheck(self):
        """ Test if service is running """
        resp = self.app.get('/healthcheck')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['message'], "Healthy")

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer_list(self):
        """ Get a list of Customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)

    def test_get_customer_by_username(self):
        """ Get customer by username """
        customer = Customer.find_by_username('jf')[0]
        resp = self.app.get('/customers?username=jf')
        data = json.loads(resp.data)
        self.assertEqual(data[0]['username'], customer.username)
        self.assertEqual(data[0]['id'], customer.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer_by_firstname(self):
        """ Get customer by firstname """
        customer = Customer.find_by_firstname('jinfan')[0]
        resp = self.app.get('/customers?firstname=jinfan')
        data = json.loads(resp.data)
        self.assertEqual(data[0]['username'], customer.username)
        self.assertEqual(data[0]['id'], customer.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)

    def test_get_customer_by_lastname(self):
        """ Get customer by lastname """
        customer = Customer.find_by_lastname('yang')[0]
        resp = self.app.get('/customers?lastname=yang')
        data = json.loads(resp.data)
        self.assertEqual(data[0]['username'], customer.username)
        self.assertEqual(data[0]['id'], customer.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)

    def test_get_customer_by_email(self):
        """ Get customer by email """
        customer = Customer.find_by_email('jy2296@nyu.edu')[0]
        resp = self.app.get('/customers?email=jy2296@nyu.edu')
        data = json.loads(resp.data)
        self.assertEqual(data[0]['id'], customer.id)
        self.assertEqual(data[0]['email'], customer.email)
        self.assertEqual(data[0]['username'], customer.username)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer_promo_list(self):
        """ Get a list of Customers with given promo status TRUE """
        customer = Customer.find_by_promo(True)
        resp = self.app.get('/customers?promo=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertTrue(len(data) == 1)

    def test_get_customer_promo_list_2(self):
        """ Get a list of Customers with given promo status FALSE """
        customer = Customer.find_by_promo(False)
        resp = self.app.get('/customers?promo=false')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertTrue(len(data) == 2)

    def test_get_customer_active_list(self):
        """ Get a list of Customers with given active status TRUE """
        customer = Customer.find_by_active(True)
        resp = self.app.get('/customers?active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertTrue(len(data) == 3)

    def test_get_customer_active_list_2(self):
        """ Get a list of Customers with given active status FALSE """
        customer = Customer.find_by_active(False)
        self.assertTrue(len(customer) == 0)
        resp = self.app.get('/customers?active=false')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        customer = Customer.find_by_username('jf')[0]
        resp = self.app.get('/customers/{}'.format(customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['username'], customer.username)

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
                        "active": True,
                        "promo": False}

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
                        "active": False,
                        "promo": False}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['active'], False)

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
                        "active": customer.active,
                        "promo": True}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}/subscribe'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['promo'], True)

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
                        "active": False,
                        "promo": customer.promo}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/{}/deactivate'.format(customer.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['active'], False)

    def test_delete_customer(self):
        """ Delete a Customer """
        customer = Customer.find_by_username('jf')[0]

        # save the current number of customers for later comparrison
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

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
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
                        "active": True,
                        "promo": False}
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
                        "active": False,
                        "promo": False}

        data = json.dumps(new_customer)
        resp = self.app.put('/customers/1000000', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_found_get_customer_by_username(self):
        """ Test a Not Found error from Find By Username """
        #not_found_mock.side_effect = server.HTTP_404_NOT_FOUND
        resp = self.app.get('/customers?username=IDONOTEXIST')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_found_get_customer_by_email(self):
        """ Test a Not Found error from Find By Email """
        #not_found_mock.side_effect = server.HTTP_404_NOT_FOUND
        resp = self.app.get('/customers?email=IDONOTEXIST')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


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
