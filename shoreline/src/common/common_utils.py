import jwt
import json

from logging import getLogger
from datetime import datetime
from flask import Response, request
from bson.objectid import ObjectId
from src.common.constants import GenericConstants as GC

logger = getLogger(__name__)


def abort(code, **kwargs):
    """ Create custom abort responses to dispatch failed requests """
    description = json.dumps(kwargs)
    return Response(status=code, mimetype='application/json',
                    response=description)


def acknowledge_request(request, event):
    """ Log received request """
    logger.info('User from client [{0}] Event [{1}] executed API '
                'on UI server[{2}]:[{3}]'.format(request.remote_addr, event,
                                                 request.url, request.method))


def acknowledge_response(status_code):
    """ Log response """
    logger.info("Dispatched response with status code: {}".format(status_code))


def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token:
            return {GC.FAULTSTRING: 'Missing token'}, 401
        if not is_valid_token(token):
            return {GC.FAULTSTRING: 'Invalid token!!'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated


def is_valid_token(token):
    """
    Helper method to validate JWT token
    """
    try:
        decoded = jwt.decode(token, GC.AUTHSECRET, algorithms=['HS256'])
        if datetime.strptime(decoded['tkn_expiry'], '%d/%m/%Y %H:%M:%S') < datetime.now():
            return False
    except Exception as e:
        return False
    return True


def is_valid_object_id(device_id):
    """
    Helper method to verify valid MongoDB ObjectID
    :param device_id: Input provided by user as DeviceID
    :return: Boolean based on the results
    """
    try:
        ObjectId(device_id)
    except Exception as e:
        return False
    return True
