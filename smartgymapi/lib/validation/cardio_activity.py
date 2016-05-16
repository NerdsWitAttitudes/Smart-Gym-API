from marshmallow import Schema, fields


class CardioActivitySchema(Schema):
    id = fields.Str(dump_only=True)
    activity_id = fields.UUID(required='Activity id is required')
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    is_active = fields.Boolean(dump_only=True)
    distance = fields.Integer()
    speed = fields.Float()
    calories = fields.Float()
