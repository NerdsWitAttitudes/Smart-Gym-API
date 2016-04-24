from marshmallow import Schema, fields


class MusicPreferenceSchema(Schema):
    id = fields.Str(dump_only=True)
    genre = fields.Str(required='Genre is required')
    artist = fields.Str()
    song_name = fields.Str()
    spotify_uri = fields.Str()
    spotify_category_id = fields.Str()
    spotify_id = fields.Str()
