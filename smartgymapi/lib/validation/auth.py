from marshmallow import Schema, fields, ValidationError, post_load, pre_load
from sqlalchemy.orm.exc import NoResultFound

from smartgymapi.lib.exceptions.auth import UserFoundException
from smartgymapi.models.user import get_user_by_email


class SignupSchema(Schema):
    password = fields.Str(required='Password is required')
    password_confirm = fields.Str(required='Password is required')

    @post_load
    def compare_passwords(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError("{'password': ['Passwords do not match']}")

    @pre_load
    def validate_email_address(self, data):
        try:
            get_user_by_email(data['email'])
        except KeyError:
            # This means there's no email address in the data. This will be
            # handled in the user validation.
            return
        except NoResultFound:
            # Meaning no user was found containing this email address.
            # We can proceed to create the new user
            return
        raise UserFoundException


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
