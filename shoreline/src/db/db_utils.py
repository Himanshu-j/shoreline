"""
Util file to hold all the DB helper methods
"""
from src.db import shoreline_db as db
from bson.objectid import ObjectId


def create_new_device(name):
    """
    Helper method to create new device and provide the name to it
    :param name: Initial name of the device
    :return: DB-Id of the newly created device
    """
    new_device = {'device': name,
                  'tsummary': {},
                  'psummary': {},
                  'temperature_sensor': [],
                  'pressure_sensor': []}
    post_id = db.devices.insert_one(new_device).inserted_id
    return str(post_id)


def update_device_by_id(device_id, name):
    """
    Helper method to update data from DB on the basis of device-id
    :param device_id: Device ID to be queried
    :param name: Updated name to the device
    :return: result of the query
    """
    res = db.devices.update_one({'_id': ObjectId(device_id)},
                                {'$set': {'device': name}})
    return res.acknowledged


def fetch_device_by_id(device_id):
    """
    Helper method to get data from DB on the basis of device-id
    :param device_id: Device ID to be queried
    :return: result of the query
    """
    res = db.devices.find_one({'_id': ObjectId(device_id)})
    res['_id'] = str(res['_id'])
    return res


def check_oid_exists(device_id):
    """
    Helper method to verify the device-id existence
    :param device_id: Device ID to be queried
    :return: Boolean based on the query result
    """
    data = db.devices.find_one({'_id': ObjectId(device_id)})
    if not data:
        return False
    return True


def update_sensor_by_type(device_id, sensor_type, start, end, sensor_data):
    """
    Helper method to update the sensor information the DB
    :param device_id: DeviceID for the update is applicable
    :param sensor_type: SensorType to which the update is applicable
    :param start: Starting timestamp of the data
    :param end: Ending timestamp of the data
    :param sensor_data: Sensor data to be updated
    :return: Boolean based on the operation results
    """
    try:
        data = db.devices.find_one({'_id': ObjectId(device_id)})
        if sensor_type.lower() == 'temperature':
            stype = 'temperature_sensor'
            summary = 'tsummary'
            resp = data.get(stype)
            curr_summary = data.get(summary)
        else:
            stype = 'pressure_sensor'
            summary = 'psummary'
            resp = data.get(stype)
            curr_summary = data.get(summary)
        dindex = len(resp)
        dkey = start + '++' + end
        dsummary = {dkey: dindex}
        rev_dsummary = {str(dindex): dkey}
        curr_summary.update(dsummary)
        curr_summary.update(rev_dsummary)
        print(curr_summary)
        resp.append(sensor_data)
        _ = db.devices.update_one({'_id': ObjectId(device_id)},
                                    {'$set': {f'{stype}': resp}})
        _ = db.devices.update_one({'_id': ObjectId(device_id)},
                                  {'$set': {f'{summary}': curr_summary}})
    except Exception as e:
        print(e)
        return False
    return True


def fetch_sensor_data_by_type(device_id, stype):
    """
    Helper method to GET all the data of given sensor
    :param device_id: DeviceID to be queried
    :param stype: SensorType to which data is required
    :return: Tuple consisting required data and summary to the data
    """
    data = fetch_device_by_id(device_id)
    if stype.lower() == 'temperature':
        curr_summary = data.get('tsummary')
        resp = data.get('temperature_sensor')
    else:
        curr_summary = data.get('psummary')
        resp = data.get('pressure_sensor')
    return resp, curr_summary


def fetch_sensor_data_by_time(device_id, stype, start, end):
    """
    Helper method to GET the sensor data based on given time frame
    :param device_id: DeviceID to be queried
    :param stype: SensorType to which data is required
    :param start: Starting timestamp of the data
    :param end: Ending timestamp of the data
    :return: Dictionary of required data
    """
    raw_data, summary = fetch_sensor_data_by_type(device_id, stype)
    dkey = start + '++' + end
    if dkey not in summary.keys():
        return []
    dindex = summary.get(dkey)
    data = {'start': start,
            'end': end,
            'data': raw_data[dindex]}
    return data

