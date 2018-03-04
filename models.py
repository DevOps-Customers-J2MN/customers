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
status (int) - the status of the customer account

"""


import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Customer(db.Model):
    """
    Class that represents a Customer

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(63), nullable=False, unique=True)
    password = db.Column(db.String(63), nullable=False)
    firstname = db.Column(db.String(63), nullable=False)
    lastname = db.Column(db.String(63), nullable=False)
    address = db.Column(db.String(123))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(63), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Customer %r>' % (self.username)

    def save(self):
        """ Saves a Customer to the data store """
        customer = Customer.find_by_username(self.username)
        if not customer:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id,
                "username": self.username,
                "password": self.password,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "address": self.address,
                "phone": self.phone,
                "email": self.email,
                "status": self.status}

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the Customer data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid customer: body of request contained bad or no data')
        try:
            self.username = data['username']
            self.password = data['password']
            self.firstname = data['firstname']
            self.lastname = data['lastname']
            self.address = data['address']
            self.phone = data['phone']
            self.email = data['email']
            self.status = data['status']
        except KeyError as error:
            raise DataValidationError('Invalid customer: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid customer: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Customer.logger.info('Initializing database')
        Customer.app = app

        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        # make our sqlalchemy tables
        db.create_all()

    @staticmethod
    def all():
        """ Returns all of the Customers in the database """
        Customer.logger.info('Processing all Customers')
        return Customer.query.all()

    @staticmethod
    def find(customer_id):
        """ Finds a Customer by it's ID """
        Customer.logger.info('Processing lookup for id %s ...', customer_id)
        return Customer.query.get(customer_id)

    @staticmethod
    def find_or_404(customer_id):
        """ Find a Customer by it's ID """
        Customer.logger.info('Processing lookup or 404 for id %s ...', customer_id)
        return Customer.query.get_or_404(customer_id)

    @staticmethod
    def find_by_username(username):
        """
        Returns a Customer with the given username

        Args:
            username (string): the username of the Customer you want to match
        """
        Customer.logger.info('Processing username query for %s ...', username)
        return Customer.query.filter(Customer.username == username)

    @staticmethod
    def find_by_email(email):
        """
        Returns a Customer with the given email

        Args:
            email (string): the email of the Customer you want to match
        """
        Customer.logger.info('Processing email query for %s ...', email)
        return Customer.query.filter(Customer.email == email)

    @staticmethod
    def find_by_status(status):
        """
        Returns all of Customers by their status

        Args:
            status (int): the status of the Customers you want to match
        """
        Customer.logger.info('Processing status query for %s ...', status)
        return Customer.query.filter(Customer.status == status)
