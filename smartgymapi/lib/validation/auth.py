from marshmallow import Schema, fields, ValidationError, post_load


class SignupSchema(Schema):
    password = fields.Str(required='Password is required')
    password_confirm = fields.Str(required='Password is required')

    @post_load
    def compare_passwords(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("{'password': ['Passwords do not match']}")
