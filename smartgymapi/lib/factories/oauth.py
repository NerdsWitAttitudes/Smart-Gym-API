import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest
from sqlalchemy.orm.exc import NoResultFound

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.lib.security import extract_client_authorization
from smartgymapi.lib.validation.oauth import GETTokenSchema, OAuthClientSchema
from smartgymapi.models.oauth import get_client

log = logging.getLogger(__name__)


class OAuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['token'] = TokenFactory(self, 'token')


class TokenFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_client(self):
        try:
            result, errors = GETTokenSchema(strict=True).load(
                self.request.json_body)

            grant_type = result['grant_type']
            client_credentials = extract_client_authorization(self.request)

            result, errors = OAuthClientSchema(
                strict=True, only=('client_id', 'client_secret')).load(
                    client_credentials)
        except ValidationError as e:
            raise HTTPBadRequest(json=str(e))

        try:
            return get_client(**result)
        except NoResultFound:
            raise HTTPBadRequest
