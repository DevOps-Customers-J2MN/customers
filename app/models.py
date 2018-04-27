"""
Models for Customer Service

All of the models are stored in this module

Models
------
Customer - A Customer used in the E-commerce website

Attributes:
-----------
id (int) - the id of the customer
username (string) - the username of the customer account
password (string) - the password to log in to customer account
first name (string) - the first name of the customer
last name (string) - the last name of the customer
address (string) - the address of the customer
phone (string) - the phone of the customer
email (string) - the email of the customer
active (boolean) - the status of the customer account
promo (boolean) - the subscription status of the customer
"""

import os
import logging
import json
import pickle
from redis import Redis
from redis.exceptions import ConnectionError
from app.custom_exceptions import DataValidationError

# Validator allow to creat a schema
from cerberus import Validator

######################################################################
# Customer Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################

class Customer(object):
    """ Customer interface to database """

    logger = logging.getLogger(__name__)
    redis = None

    schema = {
        'id': {'type': 'integer'},
        'username': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True},
        'firstname': {'type': 'string', 'required': True},
        'lastname': {'type': 'string', 'required': True},
        'address': {'type': 'string'},
        'phone': {'type': 'string'},
        'email': {'type': 'string', 'required': True},
        'active': {'type': 'boolean', 'required': True},
        'promo': {'type': 'boolean', 'required': True}
    }
    __validator = Validator(schema)

    def __init__(self, id=0, username=None, password=None, firstname=None, lastname=None, address=None, phone=None, email=None, active=True, promo=False):
        """ Constructor """
        self.id = int(id)
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.phone = phone
        self.email = email
        self.active = active
        self.promo = promo

    def __repr__(self):
        return '<Customer %r>' % (self.username)

    def save(self):
        """ Saves a Customer in the database """
        if self.username is None:
            raise DataValidationError('username is not set')
        if self.password is None:
            raise DataValidationError('password is not set')
        if self.firstname is None:
            raise DataValidationError('firstname is not set')
        if self.lastname is None:
            raise DataValidationError('lastname is not set')
        if self.email is None:
            raise DataValidationError('email is not set')
        if self.id == 0:
            self.id = Customer.__next_index()
        Customer.redis.set(self.id, pickle.dumps(self.serialize()))

    def delete(self):
        """ Deletes a Customer from the database """
        Customer.redis.delete(self.id)

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "active": self.active,
            "promo": self.promo
        }

    def deserialize(self, data):
        """ Deserializes a Customer by marshalling the data """
        if isinstance(data, dict) and Customer.__validator.validate(data):
            self.username = data['username']
            self.password = data['password']
            self.firstname = data['firstname']
            self.lastname = data['lastname']
            self.address = data['address']
            self.phone = data['phone']
            self.email = data['email']
            self.active = data['active']
            self.promo = data['promo']
        else:
            raise DataValidationError('Invalid customer data: ' + str(Customer.__validator.errors))

        return self


######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################

    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return Customer.redis.incr('index')

    @staticmethod
    def remove_all():
        """ Removes all Customers from the database """
        Customer.redis.flushall()

    @staticmethod
    def all():
        """ Query that returns all Customers """
        # results = [Customer.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in Customer.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Customer.redis.get(key))
                customer = Customer(data['id']).deserialize(data)
                results.append(customer)
        return results


######################################################################
#  F I N D E R   M E T H O D S
######################################################################

    @staticmethod
    def find(customer_id):
        """ Finds a Customer by their ID """
        if Customer.redis.exists(customer_id):
            data = pickle.loads(Customer.redis.get(customer_id))
            customer = Customer(data['id']).deserialize(data)
            return customer
        return None

    @staticmethod
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        Customer.logger.info('Processing %s query for %s', attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower() # make case insensitive
        else:
            search_criteria = value

        results = []
        for key in Customer.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Customer.redis.get(key))
                # perform case insensitive search on strings
                if isinstance(data[attribute], str):
                    test_value = data[attribute].lower()
                else:
                    test_value = data[attribute]

                if test_value == search_criteria:
                    results.append(Customer(data['id']).deserialize(data))
        return results

    @staticmethod
    def find_by_username(username):
        """ Returns a Customer with the given username

        Args:
            username (string): the username of the Customer you want to match
        """
        return Customer.__find_by('username', username)

    @staticmethod
    def find_by_email(email):
        """
        Returns a Customer with the given email

        Args:
            email (string): the email of the Customer you want to match
        """
        return Customer.__find_by('email', email)

    @staticmethod
    def find_by_active(active):
        """
        Returns all of Customers by their status

        Args:
            status (int): the status of the Customers you want to match
        """
        active = bool(active)
        return Customer.__find_by('active', active)

    @staticmethod
    def find_by_promo(promo):
        """
        Returns all of Customers by their promo

        Args:
            promo (int): the status of the Customers you want to match
        """
        promo = bool(promo)
        return Customer.__find_by('promo', promo)


######################################################################
#  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
######################################################################

    @staticmethod
    def connect_to_redis(hostname, port, password):
        """ Connects to Redis and tests the connection """
        Customer.logger.info("Testing Connection to: %s:%s", hostname, port)
        Customer.redis = Redis(host=hostname, port=port, password=password)
        try:
            Customer.redis.ping()
            Customer.logger.info("Connection established")
        except ConnectionError:
            Customer.logger.info("Connection Error from: %s:%s", hostname, port)
            Customer.redis = None
        return Customer.redis

    @staticmethod
    def init_db(redis=None):
        """
        Initialized Redis database connection

        This method will work in the following conditions:
          1) In Bluemix with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object

        Exception:
        ----------
          redis.ConnectionError - if ping() test fails
        """
        if redis:
            Customer.logger.info("Using client connection...")
            Customer.redis = redis
            try:
                Customer.redis.ping()
                Customer.logger.info("Connection established")
            except ConnectionError:
                Customer.logger.error("Client Connection Error!")
                Customer.redis = None
                raise ConnectionError('Could not connect to the Redis Service')
            return
        # Get the credentials from the Bluemix environment
        if 'VCAP_SERVICES' in os.environ:
            Customer.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ['VCAP_SERVICES']
            services = json.loads(vcap_services)
            creds = services['rediscloud'][0]['credentials']
            Customer.logger.info("Conecting to Redis on host %s port %s",
                            creds['hostname'], creds['port'])
            Customer.connect_to_redis(creds['hostname'], creds['port'], creds['password'])
        else:
            Customer.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
            Customer.connect_to_redis('127.0.0.1', 6379, None)
            if not Customer.redis:
                Customer.logger.info("No Redis on localhost, looking for redis host")
                Customer.connect_to_redis('redis', 6379, None)
        if not Customer.redis:
            # if you end up here, redis instance is down.
            Customer.logger.fatal('*** FATAL ERROR: Could not connect to the Redis Service')
            raise ConnectionError('Could not connect to the Redis Service')
