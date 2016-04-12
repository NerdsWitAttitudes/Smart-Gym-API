from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required='Email is required')
    firstname = fields.Str(required='Firstname is required')
    lastname = fields.Str(required='Lastname is required')
    infix = fields.Str(default='')
    date_created = fields.DateTime(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
    # We might want to use an external service to get country names
    country = fields.Str(required='Country is required')
    date_of_birth = fields.DatTime(required='Date of birth is required')
    last_login = fields.DateTime(dump_only=True)
