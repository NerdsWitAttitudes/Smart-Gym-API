from marshmallow import Schema, fields


class BusynessSchema(Schema):
    date = fields.Date()
