from marshmallow import Schema, fields


class SpotifySchema(Schema):
    client_address = fields.Str(required='Client address is required')
    uri = fields.Str()
