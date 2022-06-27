from flask_restx import fields


def get_sensor_model(api):
    """ Returns model of sensor """

    model = api.model('Sensor data', {
        'device_id': fields.String(required=True,
                                   description='Device ID'),
        'sensors': fields.Raw(required=True,
                              description='Sensors with data')
    })
    return model