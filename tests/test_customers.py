"""
Test cases for Customer Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from models import Customer, DataValidationError, db
from server import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomers(unittest.TestCase):
    """ Test Cases for Customers """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Customer.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """

        customer = Customer(username='jf',
                            password='12345',
                            firstname='jinfan',
                            lastname='yang',
                            address='nyu',
                            phone='123-456-7890',
                            email='jy2296@nyu.edu',
                            status=1,
                            promo=1)

        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.username, "jf")
        self.assertEqual(customer.password, '12345')
        self.assertEqual(customer.firstname, 'jinfan')
        self.assertEqual(customer.lastname, 'yang')
        self.assertEqual(customer.address, 'nyu')
        self.assertEqual(customer.phone, '123-456-7890')
        self.assertEqual(customer.email, 'jy2296@nyu.edu')
        self.assertEqual(customer.status, 1)
        self.assertEqual(customer.promo, 1)

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
                            status=1,
                            promo=1)

        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)

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
                            status=1,
                            promo=1)

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
                            status=1,
                            promo=1)

        customer.save()
        self.assertEqual(len(Customer.all()), 1)
        # delete the pet and make sure it isn't in the database
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
                            status=1,
                            promo=1)

        data = customer.serialize()

        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
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
        self.assertIn('status', data)
        self.assertEqual(data['status'], 1)
        self.assertIn('promo', data)
        self.assertEqual(data['promo'], 1)

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
                "status": 1,
                "promo": 1}

        customer = Customer()
        customer.deserialize(data)

        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.username, "jf")
        self.assertEqual(customer.password, "12345")
        self.assertEqual(customer.firstname, "jinfan")
        self.assertEqual(customer.lastname, "yang")
        self.assertEqual(customer.address, "nyu")
        self.assertEqual(customer.phone, "123-456-7890")
        self.assertEqual(customer.email, "jy2296@nyu.edu")
        self.assertEqual(customer.status, 1)
        self.assertEqual(customer.promo, 1)

    def test_find_customer(self):
        """ Find a Customer by ID """
        customer1 = Customer(username='jf',
                             password='12345',
                             firstname='jinfan',
                             lastname='yang',
                             address='nyu',
                             phone='123-456-7890',
                             email='jy2296@nyu.edu',
                             status=1,
                             promo=1)
        customer1.save()

        customer2 = Customer(username='ms',
                             password='11111',
                             firstname='mary',
                             lastname='sue',
                             address='nyu',
                             phone='123-456-7890',
                             email='marysue@gmail.com',
                             status=0,
                             promo=0)
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
        self.assertEqual(thecustomer.status, 0)
        self.assertEqual(thecustomer.promo, 0)

    def test_find_by_username(self):
        """ Find a Customer by username """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1, promo=1).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', status=0, promo=0).save()

        customers = Customer.find_by_username("jf")

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].status, 1)
        self.assertEqual(customers[0].promo, 1)

    def test_find_by_email(self):
        """ Find a Customer by email """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1, promo=1).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', status=0, promo=1).save()

        customers = Customer.find_by_email("jy2296@nyu.edu")

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].status, 1)
        self.assertEqual(customers[0].promo, 1)

    def test_find_by_status(self):
        """ Find Customers by status """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1, promo=1).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', status=0, promo=1).save()

        customers = Customer.find_by_status(1)

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].status, 1)
        self.assertEqual(customers[0].promo, 1)


    def test_find_by_promo(self):
        """ Find Customers by promo """
        Customer(username='jf', password='12345',
                 firstname='jinfan', lastname='yang',
                 address='nyu', phone='123-456-7890',
                 email='jy2296@nyu.edu', status=1, promo=1).save()

        Customer(username='ms', password='11111',
                 firstname='mary', lastname='sue',
                 address='nyu', phone='123-456-7890',
                 email='marysue@gmail.com', status=0, promo=0).save()

        customers = Customer.find_by_promo(1)

        self.assertEqual(customers[0].username, "jf")
        self.assertEqual(customers[0].password, "12345")
        self.assertEqual(customers[0].firstname, "jinfan")
        self.assertEqual(customers[0].lastname, "yang")
        self.assertEqual(customers[0].address, "nyu")
        self.assertEqual(customers[0].phone, "123-456-7890")
        self.assertEqual(customers[0].email, "jy2296@nyu.edu")
        self.assertEqual(customers[0].status, 1)
        self.assertEqual(customers[0].promo, 1)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
