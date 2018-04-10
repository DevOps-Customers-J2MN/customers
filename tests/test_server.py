
"""
Customer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import unittest
import os
import json
import logging
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch

from models import Customer, DataValidationError, db
import server

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.INFO)
        # Set up the test database
        server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables

        Customer(username='MeenakshiSundaram', password='123',
                 firstname='Meenakshi', lastname='Sundaram',
                 address='Jersey City', phone='2016604601',
                 email='msa503@nyu.edu', status=1, promo=1).save()

        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1, promo=0).save()

        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Customer REST API Service')

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
        data=json.loads(resp.data)
        self.assertEquals(data['username'],customer.username)
        self.assertEquals(data['id'],customer.id)
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

    # def test_query_pet_list_by_category(self):
    #     """ Query Pets by Category """
    #     resp = self.app.get('/pets', query_string='category=dog')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     self.assertGreater(len(resp.data), 0)
    #     self.assertIn('fido', resp.data)
    #     self.assertNotIn('kitty', resp.data)
    #     data = json.loads(resp.data)
    #     query_item = data[0]
    #     self.assertEqual(query_item['category'], 'dog')
    #
    # @patch('server.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_found_error(self):
        """ Test showing exception handling 404 """
        rv = self.app.get('/4444')
        self.assertEqual(rv.status_code, 404)

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
