"""
Customer Service
This is an example of a customer service written with Python Flask
It demonstraits how a RESTful service should be implemented.
Paths
-----
GET  /customers - Retrieves a list of Customer from the database
GET  /customers/{id} - Retrieves a Customer with a specific id
GET  /customers/{username} - Retrieves a Customer by username
POST /customers - Creates a Customer in the datbase from the posted database
PUT  /customers/{id} - Updates a Customer in the database fom the posted database
DELETE /customers/{id} - Removes a Customer from the database that matches the id
GET /customers/{promo} - Retrieves a list of Customer with the promo from the database
PUT /customers/{id}/subscribe - Subscribe a Customer with id
PUT /customers/{id}/deactivate - Deactivate a Customer with id
"""

import sys
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.models import Customer
from . import app

#from models import Customer, DataValidationError

# Create Flask application
#app = Flask(__name__)
#app.config['LOGGING_LEVEL'] = logging.INFO

# Pull options from environment
#DEBUG = (os.getenv('DEBUG', 'False') == 'True')
#PORT = os.getenv('PORT', '5000')

# Error handlers reuire app to be initialized so we must import
# then only after we have initialized the Flask app instance
import error_handlers

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    #return jsonify(name='Customer REST API Service',
    #               version='1.0',
    #               url=url_for('list_customers', _external=True)), HTTP_200_OK
    return app.send_static_file('index.html')

######################################################################
# DELETE ALL CUSTOMER DATA (for testing only)
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removes all customers from the database """
    Customer.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# LIST ALL CUSTOMERS AND QUERY
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Retrieves a list of customers from the database or query username"""
    arguments = len(request.args)
    print(arguments)
    if arguments==0:
        customers = Customer.all()
        results = [customer.serialize() for customer in customers]
        return make_response(jsonify(results), status.HTTP_200_OK)
        #results = Customer.all()
        #return jsonify([customer.serialize() for customer in results]), HTTP_200_OK
    elif 'username' in request.args:
        username = request.args['username']
        customer = Customer.find_by_username(username)
        if customer:
            customer = customer[0]
            message = customer.serialize()
            return_code = HTTP_200_OK
        else:
            message = {'error': 'Customer with username: %s was not found' % username}
            return_code = HTTP_404_NOT_FOUND
    else:
        message = {'error': 'Your request method is not supported. Only username search supported.'}
        return_code = HTTP_405_METHOD_NOT_ALLOWED

    return jsonify(message), return_code


######################################################################
# RETRIEVE A CUSTOMER By ID
######################################################################
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customers(customer_id):
    """ Retrieves a Customer with a specific id """
#    customer = Customer.find(id)
#    if customer:
#        message = customer.serialize()
#        return_code = HTTP_200_OK
#    else:
#        message = {'error' : 'Customer with id: %s was not found' % str(id)}
#        return_code = HTTP_404_NOT_FOUND
#
#    return jsonify(message), return_code

    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
#    """ Creates a Customer in the database from the posted database """
#    payload = request.get_json()
#    customer = Customer()
#    customer.deserialize(payload)
#    customer.save()
#    message = customer.serialize()
#    response = make_response(jsonify(message), HTTP_201_CREATED)
#    response.headers['Location'] = url_for('get_customers', id=customer.id, _external=True)
#    return response
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
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
            'email': request.form['email']
        }
    else:
        app.logger.info('Getting data from API call')
        data = request.get_json()
    app.logger.info(data)
    customer = Customer()
    customer.deserialize(data)
    customer.save()
    message = customer.serialize()
    location_url = url_for('get_customers', customer_id=customer.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {'Location': location_url})


######################################################################
# UPDATE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    """ Updates a Customer in the database from the posted database """
    customer = Customer.find(id)
    if customer:
        payload = request.get_json()
        customer.deserialize(payload)
        customer.id = id
        customer.save()
        return_code = HTTP_200_OK
        message = customer.serialize()
    else:
        message = {'message': 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code


######################################################################
# SUBSCRIBE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>/subscribe', methods=['PUT'])
def subscribe_customers(id):
    """ Subscribe a Customer """
    customer = Customer.find(id)
    if customer:
        customer.promo = 1;
        customer.save()
        return_code = HTTP_200_OK
        message = customer.serialize()
    else:
        message = {'message': 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code


######################################################################
# DEACTIVATE A CUSTOMER
######################################################################
@app.route('/customers/<int:id>/deactivate', methods=['PUT'])
def deactivate_customers(id):
    """ Subscribe a Customer """
    customer = Customer.find(id)
    if customer:
        customer.status= 0;
        customer.save()
        return_code = HTTP_200_OK
        message = customer.serialize()
    else:
        message = {'message': 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code


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
# LIST ALL CUSTOMERS WITH PROMO SUBSCRIPTION
######################################################################
@app.route('/customers/promo/<int:promo>', methods=['GET'])
def list_customers_promo(promo):
    """ Retrieves a list of customers with promo from the database """
    results = []
    results = Customer.find_by_promo(promo)

    return jsonify([customer.serialize() for customer in results]), HTTP_200_OK


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
        payload['email'])#,
        #payload['status'],
        #payload['promo'])
    customer.save()

def data_reset():
    """ Removes all Customers from the database """
    Customer.remove_all()

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

