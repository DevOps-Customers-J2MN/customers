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

import os
import sys
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response
from flask_api import status    # HTTP Status Codes

from models import Customer, DataValidationError

# Create Flask application
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles all data validation issues from the model """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles requests that have bad or malformed data """
    return jsonify(status=400, error='Bad Request', message=error.message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles Customers that cannot be found """
    return jsonify(status=404, error='Not Found', message=error.message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles bad method calls """
    return jsonify(status=405, error='Method not Allowed', message=error.message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles catostrophic errors """
    return jsonify(status=500, error='Internal Server Error', message=error.message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Customer REST API Service',
                   version='1.0',
                   url=url_for('list_customers', _external=True)), HTTP_200_OK

######################################################################
# LIST ALL CUSTOMERS AND QUERY
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Retrieves a list of customers from the database or query username"""
    arguments = len(request.args)
    print(arguments)
    results = []
    if arguments==0:
        results = Customer.all()
        return jsonify([customer.serialize() for customer in results]), HTTP_200_OK
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
@app.route('/customers/<int:id>', methods=['GET'])
def get_customers(id):
    """ Retrieves a Customer with a specific id """
    customer = Customer.find(id)
    if customer:
        message = customer.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Customer with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code

######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    """ Creates a Customer in the database from the posted database """
    payload = request.get_json()
    customer = Customer()
    customer.deserialize(payload)
    customer.save()
    message = customer.serialize()
    response = make_response(jsonify(message), HTTP_201_CREATED)
    response.headers['Location'] = url_for('get_customers', id=customer.id, _external=True)
    return response

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
    """ Loads a Pet into the database """
    customer = Customer(0,
        payload['username'],
        payload['password'],
        payload['firstname'],
        payload['lastname'],
        payload['address'],
        payload['phone'],
        payload['email'],
        payload['status'],
        payload['promo'])
    customer.save()

def data_reset():
    """ Removes all Pets from the database """
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


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "*********************************"
    print " C U S T O M E R  S E R V I C E "
    print "*********************************"
    initialize_logging()
    init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
