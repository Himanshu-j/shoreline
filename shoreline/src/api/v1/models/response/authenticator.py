from flask_restx import fields


def login_res_model(api):
    """ Returns model of user authentication for its response """

    auth_model = api.model('Authentication Details', {
        'token': fields.String(required=True,
                               description='Bearer token')
    })

    return auth_model
