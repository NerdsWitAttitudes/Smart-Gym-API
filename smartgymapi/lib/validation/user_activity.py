from marshmallow import Schema, fields


class UserActivitySchema(Schema):
    id = fields.Str(dump_only=True)
    gym_id = fields.Str(load_only=True, required=True)
    user_id = fields.Str(load_only=True, required=True)
    start_date = fields.DateTime(dump_only=True)
    end_date = fields.DateTime()
    minutes = fields.Integer(dump_only=True)
    day_of_week = fields.Str(dump_only=True)
