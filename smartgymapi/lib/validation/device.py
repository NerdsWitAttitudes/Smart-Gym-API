from marshmallow import Schema, fields


class DeviceSchema(Schema):
    name = fields.Str(required='Name is required')
    device_address = fields.Str(required='Device address is required')
    device_class = fields.Str(required='Device class is required')
    client_address = fields.Str(required='Client address is required')
