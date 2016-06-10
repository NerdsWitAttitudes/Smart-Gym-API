from marshmallow import Schema, fields


class MusicPreferenceSchema(Schema):
    id = fields.Str(dump_only=True)
    genre = fields.Str(required='genre is required')
