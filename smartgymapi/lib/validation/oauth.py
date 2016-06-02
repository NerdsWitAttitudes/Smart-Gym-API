from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf


class GETTokenSchema(Schema):
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
        required='client_id is required',
        validate=Length(
            equal=64,
            error='client_secret must be exactly 64 characters long')
    )
    name = fields.Str(required='name is required')
