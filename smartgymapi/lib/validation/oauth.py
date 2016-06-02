from marshmallow import Schema, fields


class GETTokenSchema(Schema):
    grant_type = fields.Str(required='grant_type is required')
