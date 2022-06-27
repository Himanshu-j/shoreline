from flask_restx import fields


def login_post_model(api):
    """ Model of user authentication for its payload """

    auth_model = api.model('Authentication Details', {
        'email_id': fields.String(required=True,
                                  description='Email-ID of user'),
        'password': fields.String(required=True,
                                  description='Password of user')
    })

    return auth_model
