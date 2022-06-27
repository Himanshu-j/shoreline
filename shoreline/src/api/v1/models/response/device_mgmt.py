from flask_restx import fields


def get_device_model(api):
    """ Returns model of GET method for device """

    res_model = api.model('Get Device Response Details', {
        'device_id': fields.Integer(required=True,
                                 description='game-id of cricket-match')
    })

    return res_model
