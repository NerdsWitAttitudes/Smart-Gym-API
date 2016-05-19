from marshmallow import Schema, fields, ValidationError, post_load, pre_load


class SignupSchema(Schema):
    password = fields.Str(required='Password is required')
    password_confirm = fields.Str(required='Password is required')

    @post_load
    def compare_passwords(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("{'password': ['Passwords do not match']}")


class LoginSchema(Schema):
    email = fields.Email(required='Email is required')
    password = fields.Str(required='Password is required')

    @pre_load
    def strip_email(self, data):
        try:
            data['email'] = data['email'].lower().strip()
        except KeyError:
            raise ValidationError('Email is required')
        return data


class CheckinSchema(Schema):
    device_address = fields.Str(required='Device address is required')
    device_class = fields.Str(required='Device class is required')
    client_address = fields.Str(required='Client address is required')
