"""
Customer Service
This is an example of a customer service written with Python Flask
It demonstraits how a RESTful service should be implemented.
Paths
-----
GET  /customers - Retrieves a list of Customer from the database
GET  /customers{id} - Retrirves a Customer with a specific id
POST /customers - Creates a Customer in the datbase from the posted database
PUT  /customers/{id} - Updates a Customer in the database fom the posted database
DELETE /customers{id} - Removes a Customer from the database that matches the id
"""

import os
import sys
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

from flask_sqlalchemy import SQLAlchemy

from models import Customer, DataValidationError

# Create Flask application
app = Flask(__name__)

# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret key'
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
    return jsonify(status=405, error='Method not Allowed',
                   message='Your request method is not supported.' \
                   ' Check your HTTP method and try again.'), 405

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
# LIST ALL CUSTOMERS
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Retrieves a list of customers from the database """
    results = []
    results = Customer.all()

    return jsonify([customer.serialize() for customer in results]), HTTP_200_OK

######################################################################
# RETRIEVE A CUSTOMER
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
    """ Creates a Customer in the datbase from the posted database """
    payload = request.get_json()
    customer = Customer()
    customer.deserialize(payload)
    customer.save()
    message = customer.serialize()
    response = make_response(jsonify(message), HTTP_201_CREATED)
    response.headers['Location'] = url_for('get_customers', id=customer.id, _external=True)
    return response


######################################################################
#   U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    "Initialies the SQLAlchemy app"
    global app
    Customer.init_db(app)


def check_content_type(content_type):
    "Checks that the medis type is correct"
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))


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
    # make sqlalchemy tables
    init_db()

    # dummy data for testing
    Customer(username='Meenakshi Sundaram', password='123', firstname='Meenakshi', lastname='Sundaram',
             address='Jersey City', phone='2016604601', email='msa503@nyu.edu', status=1).save()

    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)