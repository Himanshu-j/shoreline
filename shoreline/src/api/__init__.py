"""
This file initialises the source-code of the server
"""

from flask_restx import Api

# Import the required namespaces/modules/Resource-Controller
from src.api.v1.services.authenticator import api as auth
from src.api.v1.services.device import api as device
from src.api.v1.services.sensor import api as sensor

# Initialise the Flask-restx API and add required namespaces
api = Api(
    title='Shoreline',
    version='1.0',
    description='Shoreline Assignment'
)

api.add_namespace(auth)
api.add_namespace(device)
api.add_namespace(sensor)
