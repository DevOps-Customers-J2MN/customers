"""
Test cases for Customer Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
import json
from mock import patch
from redis import Redis, ConnectionError
from werkzeug.exceptions import NotFound
from app.models import Customer
from app.custom_exceptions import DataValidationError
from app import server

VCAP_SERVICES = os.getenv('VCAP_SERVICES', None)
if not VCAP_SERVICES:
    VCAP_SERVICES = {
        'rediscloud': [
            {'credentials': { 'password': '',
                              'hostname': '127.0.0.1',
                              'port': '6379'}
            }
        ]
    }


######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomers(unittest.TestCase):
    """ Test Cases for Customer Model"""

    def setUp(self):
        """ Initialize the Redis database """
        Customer.init_db()
        Customer.remove_all()
        # Customer.init_db(Redis(host='127.0.0.1', port=6379))


    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """

        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            active=True,
                            promo=False)

        self.assertTrue(customer != None)
        self.assertEqual(customer.id, 0)
        self.assertEqual(customer.username, "jf")
        self.assertEqual(customer.password, '12345')
        self.assertEqual(customer.firstname, 'jinfan')
        self.assertEqual(customer.lastname, 'yang')
        self.assertEqual(customer.address, 'nyu')
        self.assertEqual(customer.phone, '123-456-7890')
        self.assertEqual(customer.email, 'jy2296@nyu.edu')
        self.assertEqual(customer.active, True)
        self.assertEqual(customer.promo, False)

    def test_add_a_customer(self):
        """ Create a customer and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])

        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            active=True,
                            promo=True)

        self.assertTrue(customer != None)
        self.assertEqual(customer.id, 0)

        # Save this customer into database
        customer.save()

        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

    def test_update_a_customer(self):
        """ Update a Customer """
        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            active=True,
                            promo=False)

        customer.save()
        self.assertEqual(customer.id, 1)

        # Change it an save it
        customer.username = 'yjf'
        customer.save()

        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].username, "yjf")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            active=True,
                            promo=False)

        customer.save()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_serialize_a_customer(self):
        """ Test serialization of a Customer """
        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            active=True,
                            promo=False)

        data = customer.serialize()

        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 0)
        self.assertIn('username', data)
        self.assertEqual(data['username'], "jf")
        self.assertIn('password', data)
        self.assertEqual(data['password'], "12345")
        self.assertIn('firstname', data)
        self.assertEqual(data['firstname'], "jinfan")
        self.assertIn('lastname', data)
        self.assertEqual(data['lastname'], "yang")
        self.assertIn('address', data)
        self.assertEqual(data['address'], "nyu")
        self.assertIn('phone', data)
        self.assertEqual(data['phone'], "123-456-7890")
        self.assertIn('email', data)
        self.assertEqual(data['email'], "jy2296@nyu.edu")
        self.assertIn('active', data)
        self.assertEqual(data['active'], True)
        self.assertIn('promo', data)
        self.assertEqual(data['promo'], False)

    def test_deserialize_a_customer(self):
        """ Test deserialization of a Customer """
        data = {"id": 1,
                "username": "jf",
                "password": "12345",
                "firstname": "jinfan",
                "lastname": "yang",
                "address": "nyu",
                "phone": "123-456-7890",
                "email": "jy2296@nyu.edu",
                "active": True,
                "promo": True}

        customer = Customer()
        customer.deserialize(data)

        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, 0)
        self.assertEqual(customer.username, "jf")
        self.assertEqual(customer.password, "12345")
        self.assertEqual(customer.firstname, "jinfan")
        self.assertEqual(customer.lastname, "yang")
        self.assertEqual(customer.address, "nyu")
        self.assertEqual(customer.phone, "123-456-7890")
        self.assertEqual(customer.email, "jy2296@nyu.edu")
        self.assertEqual(customer.active, True)
        self.assertEqual(customer.promo, True)

    def test_find_customer(self):
        """ Find a Customer by ID """
        customer1 = Customer(username='jf',
                             password='12345',
                             firstname='jinfan',
                             lastname='yang',
                             address='nyu',
                             phone='123-456-7890',
                             email='jy2296@nyu.edu',
                             active=True,
                             promo=True)
        customer1.save()

        customer2 = Customer(username='ms',
                             password='11111',
                             firstname='mary',
                             lastname='sue',
                             address='nyu',
                             phone='123-456-7890',
                             email='marysue@gmail.com',
                             active=True,
                             promo=False)
        customer2.save()

        customers = Customer.all()
        thecustomer = Customer.find(customer2.id)

        self.assertIsNot(thecustomer, None)
        self.assertEqual(thecustomer.id, customer2.id)
        self.assertEqual(thecustomer.username, "ms")
        self.assertEqual(thecustomer.password, "11111")
        self.assertEqual(thecustomer.firstname, "mary")
        self.assertEqual(thecustomer.lastname, "sue")
        self.assertEqual(thecustomer.address, "nyu")
        self.assertEqual(thecustomer.phone, "123-456-7890")
        self.assertEqual(thecustomer.email, "marysue@gmail.com")
        self.assertEqual(thecustomer.active, True)
        self.assertEqual(thecustomer.promo, False)

    def test_find_by_username(self):
        """ Find a Customer by username """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', active=True, promo=False).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', active=True, promo=True).save()

        customers = Customer.find_by_username("jf")

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].active, True)
        self.assertEqual(customers[0].promo, False)

    def test_find_by_email(self):
        """ Find a Customer by email """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', active=True, promo=False).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', active=True, promo=True).save()

        customers = Customer.find_by_email("jy2296@nyu.edu")

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].active, True)
        self.assertEqual(customers[0].promo, False)

    def test_find_by_active(self):
        """ Find Customers by active status """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', active=True, promo=False).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', active=False, promo=True).save()

        customers = Customer.find_by_active(True)

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].active, True)
        self.assertEqual(customers[0].promo, False)

    def test_find_by_promo(self):
        """ Find Customers by promo """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', active=True, promo=False).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', active=False, promo=True).save()

        customers = Customer.find_by_promo(True)

        self.assertEqual(customers[0].username, "ms")
        self.assertEqual(customers[0].password, "11111")
        self.assertEqual(customers[0].firstname, "mary")
        self.assertEqual(customers[0].lastname, "sue")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "marysue@gmail.com")
        self.assertEqual(customers[0].active, False)
        self.assertEqual(customers[0].promo, True)

    def test_save_customer_with_no_username(self):
        """ Save a Customer with no username """
        customer = Customer(0, password='2345',
                 firstname='jahnavi', lastname='kalyani',
                 address='seattle', phone='987-456-0123',
                 email='jk5667@nyu.edu', active=True, promo=False)
        self.assertRaises(DataValidationError, customer.save)

    def test_save_customer_with_no_password(self):
        """ Save a Customer with no password """
        customer = Customer(0, username='jk', firstname='jahnavi',
                 lastname='kalyani', address='seattle',
                 phone='987-456-0123', email='jk5667@nyu.edu',
                 active=True, promo=False)
        self.assertRaises(DataValidationError, customer.save)

    def test_save_customer_with_no_firstname(self):
        """ Save a Customer with no firstname """
        customer = Customer(0, username='jk', password='2345',
                 lastname='kalyani', address='seattle',
                 phone='987-456-0123', email='jk5667@nyu.edu',
                 active=True, promo=False)
        self.assertRaises(DataValidationError, customer.save)

    def test_save_customer_with_no_lastname(self):
        """ Save a Customer with no lastname """
        customer = Customer(0, username='jk', password='2345',
                 firstname='jahnavi', address='seattle',
                 phone='987-456-0123', email='jk5667@nyu.edu',
                 active=True, promo=False)
        self.assertRaises(DataValidationError, customer.save)

    def test_save_customer_with_no_email(self):
        """ Save a Customer with no email """
        customer = Customer(0, username='jk', password='2345',
                 firstname='jahnavi', lastname='kalyani',
                 address='seattle', phone='987-456-0123',
                 active=True, promo=False)
        self.assertRaises(DataValidationError, customer.save)

    def test_save_customer_with_no_active(self):
        """ Save a Customer with no active status """
        customer = Customer(0, username='jk', password='2345',
                 firstname='jahnavi', lastname='kalyani',
                 address='seattle', phone='987-456-0123',
                 email='jk5667@nyu.edu', promo=False)
        customer.save()

        thecustomer = Customer.find(customer.id)
        self.assertIsNot(thecustomer, None)
        self.assertEqual(thecustomer.id, customer.id)
        self.assertEqual(thecustomer.active, True)

    def test_save_customer_with_no_promo(self):
        """ Save a Customer with no promo status """
        customer = Customer(0, username='jk', password='2345',
                 firstname='jahnavi', lastname='kalyani',
                 address='seattle', phone='987-456-0123',
                 email='jk5667@nyu.edu', active=True)
        customer.save()

        thecustomer = Customer.find(customer.id)
        self.assertIsNot(thecustomer, None)
        self.assertEqual(thecustomer.id, customer.id)
        self.assertEqual(thecustomer.promo, False)

    def test_customer_not_found(self):
        """ Find a Customer that doesnt exist """
        Customer(0, username='jk', password='2345',
                 firstname='jahnavi', lastname='kalyani',
                 address='seattle', phone='987-456-0123',
                 email='jk5667@nyu.edu', active=True, promo=False).save()
        customer = Customer.find(2)
        self.assertIs(customer, None)

    def test_deserialize_with_no_data(self):
        """ Deserialize a Customer that has no data """
        customer = Customer(0)
        self.assertRaises(DataValidationError, customer.deserialize, None)

    def test_deserialize_with_bad_data(self):
        """ Deserialize a Customer that has bad data """
        customer = Customer(0)
        self.assertRaises(DataValidationError, customer.deserialize, "string data")

    def test_passing_connection(self):
        """ Pass in the Redis connection """
        Customer.init_db(Redis(host='127.0.0.1', port=6379))
        self.assertIsNotNone(Customer.redis)

    def test_passing_bad_connection(self):
        """ Pass in a bad Redis connection """
        self.assertRaises(ConnectionError, Customer.init_db, Redis(host='127.0.0.1', port=6300))
        self.assertIsNone(Customer.redis)

    @patch.dict(os.environ, {'VCAP_SERVICES': json.dumps(VCAP_SERVICES)})
    def test_vcap_services(self):
        """ Test if VCAP_SERVICES works """
        Customer.init_db()
        self.assertIsNotNone(Customer.redis)

    @patch('redis.Redis.ping')
    def test_redis_connection_error(self, ping_error_mock):
        """ Test a Bad Redis connection """
        ping_error_mock.side_effect = ConnectionError()
        self.assertRaises(ConnectionError, Customer.init_db)
        self.assertIsNone(Customer.redis)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
