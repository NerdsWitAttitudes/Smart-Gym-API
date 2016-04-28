from marshmallow import Schema, fields


class SportScheduleSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.UUID(required='User id is required', default=None)
    name = fields.Str(required='Name is required')
    reminder_minutes = fields.Integer(required='Reminder is required')
