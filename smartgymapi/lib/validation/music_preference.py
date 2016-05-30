from marshmallow import Schema, fields


class MusicPreferenceSchema(Schema):
    id = fields.Str(dump_only=True)
    artist = fields.Str(required='artist is required')
