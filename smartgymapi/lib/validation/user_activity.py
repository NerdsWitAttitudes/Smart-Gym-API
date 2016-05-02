from marshmallow import Schema, fields


class UserActivitySchema(Schema):
    id = fields.Str(dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    minutes = fields.Integer()
