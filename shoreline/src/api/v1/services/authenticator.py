"""
This file can be extended to handle all the authorisation controls
"""
from flask_restx import Namespace, Resource

from logging import getLogger
from src.common import exception
from src.common import common_utils as utility
from src.api.v1.objects.Authenticator import UserAuth
from src.api.v1.models.response import authenticator as user_auth_response

logger = getLogger(__name__)
api = Namespace('Auth', description='Shoreline authentication operations')

# Response models
login_res_model = user_auth_response.login_res_model(api)


@api.route('/login')
class LoginController(Resource):
    @api.response(200, 'Success', login_res_model)
    @api.response(400, 'Bad request')
    @api.response(409, 'Conflict in performing request')
    @api.response(401, 'Unauthorized')
    def post(self):
        """ User authentication resource controller"""
        try:
            event = "New user Logging-in"
            logger.info(event)
            user_auth = UserAuth()
            response = user_auth.login()
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)
