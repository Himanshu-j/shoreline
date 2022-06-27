import jwt
import json

from flask import Response
from logging import getLogger
from src.common import exception
from datetime import datetime, timedelta
from src.common.constants import GenericConstants as GC

logger = getLogger(__name__)


class UserAuth(object):
    @staticmethod
    def login():
        """
        Method for authenticating users
        :return: response object in json
        """
        # Authentication checks
        try:
            # Generate JWT-token and response-object
            tkn_expiry = datetime.now() + timedelta(seconds=GC.JWT_EXPIRATION_TIME)
            token_expiry = tkn_expiry.strftime('%d/%m/%Y %H:%M:%S')
            res_payload = {"tkn_expiry": token_expiry}
            encoded_jwt = jwt.encode(res_payload, GC.AUTHSECRET, algorithm='HS256')
            token = encoded_jwt.decode('utf-8')
            response_object = {'token': token}
            return Response(response=json.dumps(response_object), status=200,
                            mimetype=GC.MIMETYPE)
        except Exception as err:
            logger.error(err)
            raise exception.InvalidCredentials()
