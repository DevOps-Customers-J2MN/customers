"""
Customer Service
This is an example of a customer service written with Python Flask
It demonstraits how a RESTful service should be implemented.

Paths:
-----
GET  / - Display a UI for Selenium testing
GET  /customers - Retrieves a list of all Customers from the database
GET  /customers/{id} - Retrieves a Customer with a given id number
GET  /customers?username={username} - Retrieves a Customer with a given username
GET  /customers?email={email} - Retrieves a Customer with a given email
GET  /customers?promo={true/false} - Retrieves a list of Customers with given promotion status
GET  /customers?active={true/false} - Retrieves a list of Customers with given status
POST /customers - Creates a new Customer record in the datbase
PUT  /customers/{id} - Updates a Customer record in the database
PUT  /customers/{id}/subscribe - Subscribe a Customer with id
PUT  /customers/{id}/deactivate - Deactivate a Customer with id
DELETE  /customers/{id} - Removes a Customer from the database
"""

import sys
import logging
from flask import jsonify, request, json, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.models import Customer
from . import app

# Error handlers require app to be initialized so we must import
# then only after we have initialized the Flask app instance
import error_handlers

# Swagger
from flasgger import Swagger

# Configure Swagger before initilaizing it
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "DevOps Swagger Customer App",
            "description": "This is a sample Customer server.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Check the service is still running """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return instructions """
    #return jsonify(name='Customer REST API Service',
    #               version='1.0',
    #               url=url_for('list_customers', _external=True)), HTTP_200_OK
    return app.send_static_file('index.html')


######################################################################
# LIST ALL CUSTOMERS AND QUERY
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Retrieves a list of all customers from the database """

    # yml files start with '---'
    # definitions can only define once, then you can use $ref to use it
    """
    Retrieve a list of Customers
    This endpoint will return all Customers unless a query parameter is specificed
    ---
    tags:
      - Pets
    description: The Customers endpoint allows you to query Customers
    parameters:
      - name: username
        in: query
        description: the username of Customer you are looking for
        required: false
        type: string
      - name: firstname
        in: query
        description: the firstname of Customer you are looking for
        required: false
        type: string
      - name: lastname
        in: query
        description: the lastname of Customer you are looking for
        required: false
        type: string

    definitions:
      Pet:
        type: object
        properties:
          id:
            type: integer
            description: unique id assigned internallt by service
          name:
            type: string
            description: the pets's name
          category:
            type: string
            description: the category of pet (e.g., dog, cat, fish, etc.)
    responses:
      200:
        description: An array of Customers
        schema:
          type: array
          items:
            schema:
              $ref: '#/definitions/Pet'
    """

    customers = []
    username = request.args.get('username')
    email = request.args.get('email')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    promos = request.args.get('promo')
    actives = request.args.get('active')

    if username:
        customers = Customer.find_by_username(username)
        if not customers:
            raise NotFound("Customer with username '{}' was not found.".format(username))
    elif email:
        customers = Customer.find_by_email(email)
        if not customers:
            raise NotFound("Customer with email '{}' was not found.".format(email))
    elif firstname:
        customers = Customer.find_by_firstname(firstname)
        if not customers:
            raise NotFound("Customer with firstname '{}' was not found.".format(firstname))
    elif lastname:
        customers = Customer.find_by_lastname(lastname)
        if not customers:
            raise NotFound("Customer with lastname '{}' was not found.".format(lastname))
    elif promos:
        promos = promos.lower()
        if promos == 'true':
            promo = True
        elif promos == 'false':
            promo = False
        else:
            raise ValueError
        customers = Customer.find_by_promo(promo)
        if not customers:
            raise NotFound("Customer with promotion status '{}' was not found.".format(promo))
    elif actives:
        actives = actives.lower()
        if actives == 'true':
            active = True
        elif actives == 'false':
            active = False
        else:
            raise ValueError
        customers = Customer.find_by_active(active)
        if not customers:
            raise NotFound("Customer with active status '{}' was not found.".format(active))
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A CUSTOMER BY ID
######################################################################
@app.route('/customers/<int:id>', methods=['GET'])
def get_customers(id):
    """ Retrieves a Customer with a given id number """
    customer = Customer.find(id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(id))

    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    """ Creates a Customer in the database """
    data = {}
    # Check for form submission data
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        app.logger.info('Getting data from form submit')
        data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'firstname': request.form['firstname'],
            'lastname': request.form['lastname'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'email': request.form['email'],
            'active': True,
            'promo': False
        }
    else:
        app.logger.info('Getting data from API call')
        data = request.get_json()
    app.logger.info(data)
    customer = Customer()
    customer.deserialize(data)
    customer.save()
    message = customer.serialize()
    location_url = url_for('get_customers', id=customer.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {'Location': location_url})


######################################################################
# UPDATE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    """ Updates a Customer in the database from the posted database """
    check_content_type('application/json')
    customer = Customer.find(id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(id))

    data = request.get_json()
    app.logger.info(data)
    customer.deserialize(data)
    customer.id = id
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# SUBSCRIBE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>/subscribe', methods=['PUT'])
def subscribe_customers(id):
    """ Subscribe a Customer """
    customer = Customer.find(id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(id))

    customer.promo = True
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DEACTIVATE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>/deactivate', methods=['PUT'])
def deactivate_customers(id):
    """ Deactivate a Customer """
    customer = Customer.find(id)
    if not customer:
        abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(id))

    customer.active = False
    customer.save()
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customers(id):
    """ Deletes a Customer in the database """
    customer = Customer.find(id)
    if customer:
        customer.delete()

    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE ALL CUSTOMER DATA (for testing only)
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removes all customers from the database """
    Customer.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
#   U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db(redis=None):
    """ Initlaize the model """
    Customer.init_db(redis)


def data_load(payload):
    """ Loads a Customer into the database """
    customer = Customer(0,
        payload['username'],
        payload['password'],
        payload['firstname'],
        payload['lastname'],
        payload['address'],
        payload['phone'],
        payload['email'],
        payload['active'],
        payload['promo'])
    customer.save()


def data_reset():
    """ Removes all Customers from the database """
    Customer.remove_all()


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')
