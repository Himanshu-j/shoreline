from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.objects.Device_mgmt import DeviceMgmt
from src.common import common_utils as utility
from src.api.v1.models.payload import device_mgmt as payloads
from src.api.v1.models.response import device_mgmt as responses
from src.common.common_utils import token_required
from src.common import exception
from logging import getLogger

logger = getLogger(__name__)

api = Namespace('Device', description='Shoreline Device operations')

# Payload models
post_payload = payloads.create_device_model(api)
put_payload = payloads.update_device_model(api)

# Response models
res_model = responses.get_device_model(api)

parser = reqparse.RequestParser()
parser.add_argument('device_id', location='args', required=True)
parser.add_argument('authorization', location='headers', required=True)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('authorization', location='headers', required=True)


@api.route('/device')
class DeviceController(Resource):
    # This line will enforce and verify the token-required for the API execution
    decorators = [token_required]

    @api.doc(parser=auth_parser, body=post_payload)
    @api.response(201, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Conflict in performing request')
    def post(self):
        """ API to Register new devices """
        try:
            request_payload = request.get_json()
            event = f"Registering New Device. Received data: {request_payload}"
            utility.acknowledge_request(request, event)
            reg = DeviceMgmt()
            response = reg.post(request_payload)
            utility.acknowledge_response(response.status)
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)

    @api.doc(parser=auth_parser, body=put_payload)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Conflict in performing request')
    def put(self):
        """ API to Update Registered device """
        try:
            request_payload = request.get_json()
            event = f"Updating Device. Received data: {request_payload}"
            utility.acknowledge_request(request, event)
            reg = DeviceMgmt()
            response = reg.put(request_payload)
            utility.acknowledge_response(response.status)
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)

    @api.response(200, 'Success', res_model)
    @api.response(400, 'Bad Request')
    @api.response(409, 'Conflict in performing request')
    @api.doc(parser=parser, params={"device_id": "Device ID"})
    def get(self):
        """ API to Get Registered device """
        try:
            device_id = request.args.get('device_id', '')
            event = f"Updating Device. Received data: {device_id}"
            utility.acknowledge_request(request, event)
            reg = DeviceMgmt()
            response = reg.get(device_id)
            utility.acknowledge_response(response.status)
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)
