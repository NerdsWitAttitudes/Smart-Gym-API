from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class OAuthAccessTokenSchema(Schema):
    access_token = fields.Str(dump_only=True)
    expires_in = fields.Integer(dump_only=True)
    token_type = fields.Str(dump_only=True)
    grant_type = fields.Str(
        required='grant_type is required',
        validate=OneOf(
            ('client_credentials,'),
            error='grant_type must be set to one of the following: {choices}')
    )




class OAuthClientSchema(Schema):
    id = fields.UUID(dump_only=True)
    client_id = fields.UUID(required='client_id is required')
    client_secret = fields.Str(
        required='client_secret is required',
        validate=Length(
            equal=64,
            error='client_secret must be exactly 64 characters long')
    )
    client_type = fields.Str(
        required='client_type is required',
        validate=OneOf(
            ('confidential', 'public'),
            error='client_type must be set to one of the following: '
            '{choices}'))
    name = fields.Str(required='name is required')
