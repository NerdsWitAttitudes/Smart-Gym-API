import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.lib.validation.oauth import GETTokenSchema, OAuthClientSchema

log = logging.getLogger(__name__)


class OAuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['client_credentials'] = ClientCredentialsFactory(
            self,
            'client_credentials')

    def __getitem__(self, key):
        try:
            result, errors = GETTokenSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        return self[result['grant_type']]


class ClientCredentialsFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        try:
            result, errors = OAuthClientSchema(
                strict=True, only=('client_id', 'client_secret'))
