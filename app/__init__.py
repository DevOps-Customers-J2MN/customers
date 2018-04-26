from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Load Configurations
app.config.from_object('config')

# Need to create the application first before import other modules
import server
import models
import custom_exceptions
