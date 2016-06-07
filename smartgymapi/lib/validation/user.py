from marshmallow import Schema, ValidationError, fields


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(required='Email is required')
    first_name = fields.Str(required='Firstname is required')
    last_name = fields.Str(required='Lastname is required')
    date_created = fields.DateTime(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
    # We might want to use an external service to get country names
    country = fields.Str(required='Country is required')
    date_of_birth = fields.DateTime(required='Date of birth is required')
    last_login = fields.DateTime(dump_only=True)


class BuddySchema(Schema):
    user_id = fields.UUID(required='user_id is required')

    def validate_user_id(self, data, current_user_id):
        """ Checks if the user isn't trying to befriend him or herself."""
        if data['user_id'] == current_user_id:
            raise ValidationError("You can not add yourself as a buddy")
