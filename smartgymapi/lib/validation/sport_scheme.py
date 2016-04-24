from marshmallow import Schema, fields


class SportScheduleSchema(Schema):
    user_id = fields.Integer(required='Id is required')
    name = fields.Str(required='Name is required')
    reminder_minutes = fields.Integer(required='Reminder is required')