from flask_restx import fields


def create_device_model(api):
    """
    """
    model = api.model('Register Device', {
        'name': fields.String(required=True,
                              description="Display Name for Device")
    })
    return model


def update_device_model(api):
    """
    """
    model = api.model('Update Device', {
        'name': fields.String(required=True,
                              description="Display Name for Device"),
        'device_id': fields.String(required=True, description="Device ID")
    })
    return model
