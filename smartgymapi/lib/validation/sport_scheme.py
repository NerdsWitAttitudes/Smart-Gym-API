from dateutil.parser import parse

from marshmallow import Schema, fields, ValidationError, validates


class SportScheduleSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.UUID(required='User id is required')
    name = fields.Str(required='Name is required')
    reminder_minutes = fields.Integer(required='Reminder is required')
    time = fields.Str(required='Time is required')
    weekdays = fields.List(fields.Integer(), required='Weekday is required')
    is_active = fields.Boolean(default=True)

    @validates('time')
    def validate_time(self, time_):
        try:
            parse(time_)
        except:
            raise ValidationError(time_ + ' Is not a valid time')

    @validates('weekdays')
    def validate_weekday(self, weekdays):
        for weekday in weekdays:
            if weekday > 7:
                raise ValidationError('Weekdays are not valid')
