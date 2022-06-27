from flask_restx import fields


def update_sensor_model(api):
    """
    Update Sensor objects payload
    """

    device_id = "Device ID to be updated"
    sensor_type = "Type of sensor"
    sensor_data = "Dict of time-value mapped data to be updated"
    start_date = "Start timestamp of data"
    end_date = "End timestamp of data"

    model = api.model('Update Sensor', {
        'device_id': fields.String(required=True, description=device_id),
        'sensor_type': fields.String(required=True, description=sensor_type),
        'start': fields.String(required=True, description=start_date),
        'end': fields.String(required=True, description=end_date),
        'sensor_data': fields.List(fields.String, required=True,
                                   description=sensor_data)
    })
    return model
