from marshmallow import Schema, fields


class CheckinSchema(Schema):
    device_address = fields.Str(required='Device address is required')
    device_class = fields.Str(required='Device class is required')
    client_address = fields.Str(required='Client address is required')
