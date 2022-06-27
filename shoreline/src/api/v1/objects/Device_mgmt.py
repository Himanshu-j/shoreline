import json

from flask import Response
from logging import getLogger
from src.db import db_utils as orm
from src.common.common_utils import is_valid_object_id
from src.common.constants import GenericConstants as GC

logger = getLogger(__name__)


class DeviceMgmt(object):

    @staticmethod
    def post(request_payload):
        """
        :param request_payload
        :return:
        """

        # Get user object from db
        name = request_payload['name']
        device_id = orm.create_new_device(name)
        if device_id:
            return Response(response=json.dumps({'device_id': device_id}),
                            status=200, mimetype=GC.MIMETYPE)
        else:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.FAILED_TO_CREATE_DEVICE}),
                            status=400, mimetype=GC.MIMETYPE)

    @staticmethod
    def put(request_payload):
        """
        :param request_payload
        :return:
        """
        # Get data from request payload
        name = request_payload['name']
        device_id = request_payload['device_id']

        # Sanity Checks to validate request
        if not is_valid_object_id(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)
        if not orm.check_oid_exists(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)

        # Update the device info in the DB and return suitable reponse object
        updated = orm.update_device_by_id(device_id, name)
        if updated:
            return Response(response=json.dumps({GC.MESSAGE: GC.DEVICE_UPDATED}),
                            status=200, mimetype=GC.MIMETYPE)
        else:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.FAILED_TO_UPDATE_DEVICE}),
                            status=400, mimetype=GC.MIMETYPE)

    @staticmethod
    def get(device_id):
        """
        This method will validate and serve the required data to the
        GET request on device API
        :param device_id: Device ID of devices to which details are required
        :return: the response object
        """
        # Sanity Checks to validate request
        if not is_valid_object_id(device_id):
            return Response(response=json.dumps(
                    {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                    status=400, mimetype=GC.MIMETYPE)
        if not orm.check_oid_exists(device_id):
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.INVALID_DEVICE_ID}),
                            status=400, mimetype=GC.MIMETYPE)

        # Fetch data from the DB and return the suitable response object
        device_data = orm.fetch_device_by_id(device_id)
        if device_data:
            return Response(response=json.dumps({'data': device_data}),
                            status=200, mimetype=GC.MIMETYPE)
        else:
            return Response(response=json.dumps(
                {GC.FAULTSTRING: GC.FAILED_TO_FETCH_DEVICE}),
                            status=400, mimetype=GC.MIMETYPE)

