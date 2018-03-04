
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

        Customer(username='Meenakshi Sundaram', password='123',
                 firstname='Meenakshi', lastname='Sundaram',
                 address='Jersey City', phone='2016604601',
                 email='msa503@nyu.edu', status=1).save()

        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1).save()

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

    def test_get_pet_list(self):
        """ Get a list of Customers """
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_pet(self):
        """ Get a single Customer """
        # get the id of a pet
        customer = Customer.find_by_username('jf')[0]
        resp = self.app.get('/customers/{}'.format(customer.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['username'], customer.username)

    def test_get_pet_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get('/customers/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_create_pet(self):
    #     """ Create a new Pet """
    #     # save the current number of pets for later comparison
    #     pet_count = self.get_pet_count()
    #     # add a new pet
    #     new_pet = {'name': 'sammy', 'category': 'snake', 'available': 'True'}
    #     data = json.dumps(new_pet)
    #     resp = self.app.post('/pets', data=data, content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     # Make sure location header is set
    #     location = resp.headers.get('Location', None)
    #     self.assertTrue(location != None)
    #     # Check the data is correct
    #     new_json = json.loads(resp.data)
    #     self.assertEqual(new_json['name'], 'sammy')
    #     # check that count has gone up and includes sammy
    #     resp = self.app.get('/pets')
    #     # print 'resp_data(2): ' + resp.data
    #     data = json.loads(resp.data)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(data), pet_count + 1)
    #     self.assertIn(new_json, data)
    #
    # def test_update_pet(self):
    #     """ Update an existing Pet """
    #     pet = Pet.find_by_name('kitty')[0]
    #     new_kitty = {'name': 'kitty', 'category': 'tabby', 'available': 'True'}
    #     data = json.dumps(new_kitty)
    #     resp = self.app.put('/pets/{}'.format(pet.id), data=data, content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     new_json = json.loads(resp.data)
    #     self.assertEqual(new_json['category'], 'tabby')
    #
    # def test_delete_pet(self):
    #     """ Delete a Pet """
    #     pet = Pet.find_by_name('fido')[0]
    #     # save the current number of pets for later comparrison
    #     pet_count = self.get_pet_count()
    #     resp = self.app.delete('/pets/{}'.format(pet.id),
    #                            content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(len(resp.data), 0)
    #     new_count = self.get_pet_count()
    #     self.assertEqual(new_count, pet_count - 1)
    #
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
    #
    # @patch('server.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
# Utility functions
######################################################################

    def get_customers_count(self):
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
