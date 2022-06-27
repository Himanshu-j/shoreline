import json

from flask import Response
from datetime import datetime
from logging import getLogger
from src.db import db_utils as orm
from src.common.constants import GenericConstants as GC
from src.common.common_utils import is_valid_object_id

logger = getLogger(__name__)


class SensorMgmt(object):

    @staticmethod
    def put(request_payload):
        """
        :param request_payload
        :return:
        """
        # Get data from request-payload
        device_id = request_payload['device_id']
        sensor_type = request_payload['sensor_type']
        sensor_data = request_payload['sensor_data']
        start = request_payload['start']
        end = request_payload['end']

        # Sanity checks to validate request
        if not is_valid_object_id(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)
        if not orm.check_oid_exists(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)
        if sensor_type.lower() not in ['temperature', 'pressure']:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_SENSOR_TYPE}),
                status=400, mimetype=GC.MIMETYPE)
        if start and isinstance(start, str):
            try:
                datetime.strptime(start, '%d/%m/%Y %H:%M:%S')
            except Exception as e:
                return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.INVALID_TIMESTAMP}),
                    status=400, mimetype=GC.MIMETYPE)
        if end and isinstance(end, str):
            try:
                datetime.strptime(end, '%d/%m/%Y %H:%M:%S')
            except Exception as e:
                return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.INVALID_TIMESTAMP}),
                    status=400, mimetype=GC.MIMETYPE)

        # Update the provided data in the DB
        updated = orm.update_sensor_by_type(device_id, sensor_type,
                                            start, end, sensor_data)
        if updated:
            return Response(response=json.dumps({GC.MESSAGE: GC.SENSOR_UPDATED}),
                            status=200, mimetype=GC.MIMETYPE)
        else:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.FAILED_TO_UPDATE_SENSOR}),
                            status=400, mimetype=GC.MIMETYPE)

    def get(self, device_id, stype, start=None, end=datetime.now()):
        """
        :param device_id:
        :param end:
        :param start:
        :return:
        """
        # Sanity Checks to validate the request
        if not is_valid_object_id(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)
        if not orm.check_oid_exists(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)
        if stype.lower() not in ['temperature', 'pressure']:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_SENSOR_TYPE}),
                status=400, mimetype=GC.MIMETYPE)
        if start and isinstance(start, str):
            try:
                datetime.strptime(start, '%d/%m/%Y %H:%M:%S')
            except Exception as e:
                return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.INVALID_TIMESTAMP}),
                    status=400, mimetype=GC.MIMETYPE)
        if end and isinstance(end, str):
            try:
                datetime.strptime(end, '%d/%m/%Y %H:%M:%S')
            except Exception as e:
                return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.INVALID_TIMESTAMP}),
                    status=400, mimetype=GC.MIMETYPE)

        # Fetch data based on provided information
        # 'if' block to fetch data based on provided time-frame
        # 'else' block to fetch all the data of the provided sensor
        if start:
            data = orm.fetch_sensor_data_by_time(device_id, stype, start, end)
            if not data:
                return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.DATA_NOT_FOUND}),
                    status=400, mimetype=GC.MIMETYPE)
        else:
            raw_data, summary = orm.fetch_sensor_data_by_type(device_id, stype)
            # Create time-data map for setting clear data relations at
            # the client side
            data = self.create_time_data_map(raw_data, summary)
        return Response(response=json.dumps({'sensor_data': data}),
                        status=200, mimetype=GC.MIMETYPE)

    @staticmethod
    def create_time_data_map(raw_data, summary):
        """
        Helper method to create time-data map
        :param raw_data: Raw data fetched from DB
        :param summary: Summary to the raw-data fetched from DB
        :return: list of maps
        """
        final_data = []
        for i in range(len(raw_data)):
            timestamps = summary.get(str(i), '')
            if timestamps:
                data = {'start': timestamps.split('++')[0],
                        'end': timestamps.split('++')[1],
                        'data': raw_data[i]}
                final_data.append(data)
        return final_data
