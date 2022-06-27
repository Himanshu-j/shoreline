from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.objects.Sensor_mgmt import SensorMgmt
from src.common import common_utils as utility
from src.api.v1.models.payload import sensor_mgmt as payloads
from src.api.v1.models.response import sensor_mgmt as responses
from src.common.common_utils import token_required
from src.common import exception
from logging import getLogger

logger = getLogger(__name__)

api = Namespace('Sensor', description='Shoreline Sensor operations')

# Payload models
update_sensor_payload = payloads.update_sensor_model(api)

# Response models
res_model = responses.get_sensor_model(api)

parser = reqparse.RequestParser()

parser.add_argument('authorization', location='headers', required=True)
parser.add_argument('device_id', location='args', required=True)
parser.add_argument('sensor_type', location='args', required=True)
parser.add_argument('start', location='args', required=False)
parser.add_argument('end', location='args', required=False)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('authorization', location='headers', required=True)


@api.route('/sensor')
class SensorController(Resource):
    # decorators = [token_required]

    @api.doc(parser=auth_parser, body=update_sensor_payload)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Conflict in performing request')
    def put(self):
        """ API to Update Registered sensor """
        try:
            request_payload = request.get_json()
            event = f"Updating Device. Received data: {request_payload}"
            utility.acknowledge_request(request, event)
            reg = SensorMgmt()
            response = reg.put(request_payload)
            utility.acknowledge_response(response.status)
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)

    @api.doc(parser=parser,
             params={"device_id": "Device ID",
                     "sensor_type": "'temperature' OR 'pressure'",
                     "start": "Timestamp from data is required. "
                              "Default when sensor was created. "
                              "Allowed format '%d/%m/%Y %H:%M:%S'",
                     "end": "Timestamp until when data is required. "
                            "Default is now. "
                            "Allowed format '%d/%m/%Y %H:%M:%S'"})
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Conflict in performing request')
    def get(self):
        """ API to Get Registered sensor """
        try:
            device_id = request.args.get('device_id')
            stype = request.args.get('sensor_type')
            start = request.args.get('start')
            end = request.args.get('end')
            event = f"Fetching Sensor info. Received data: {request.args}"
            utility.acknowledge_request(request, event)
            sensor = SensorMgmt()
            response = sensor.get(device_id, stype, start, end)
            utility.acknowledge_response(response.status)
            return response
        except exception.ShorelineException as e:
            return utility.abort(e.code, faultstring=e.faultstring)
