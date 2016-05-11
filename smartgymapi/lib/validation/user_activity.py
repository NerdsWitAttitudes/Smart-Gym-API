from marshmallow import Schema, fields


class UserActivitySchema(Schema):
    id = fields.Str(dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    minutes = fields.Integer(dump_only=True)
    day_of_week = fields.Str(dump_only=True)
