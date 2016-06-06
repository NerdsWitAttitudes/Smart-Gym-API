import datetime
import logging
import uuid

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.encrypt import get_secure_token
from smartgymapi.lib.validation.oauth import (OAuthAccessTokenSchema,
                                              OAuthClientSchema)
from smartgymapi.models import commit, persist, rollback
from smartgymapi.models.oauth import OAuthClient, OAuthAccessToken

log = logging.getLogger(__name__)


@view_defaults(containment='smartgymapi.lib.factories.oauth.OAuthFactory',
               permission='token',
               renderer='json')
class OAuthTokenHandler(object):
    def __init__(self, request):
        self.request = request

    @view_config(
        context='smartgymapi.lib.factories.oauth.TokenFactory')
    def post(self):
        try:
            result, errors = OAuthAccessTokenSchema(strict=True).load(
                self.request.json_body)
            grant_type = result['grant_type']
        except ValidationError as e:
            raise HTTPBadRequest(json=str(e))

        client = self.request.context.get_client(grant_type)

        token = OAuthAccessToken()
        token.access_token = get_secure_token()
        token.client = client
        token.expiry_date = (datetime.datetime.now(datetime.timezone.utc) +
                             datetime.timedelta(hours=1))
        token.token_type = 'Bearer'

        try:
            persist(token)
            response_body = OAuthAccessTokenSchema().dump(token).data
        except:
            log.critical("Something went wrong saving the token",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

        # response headers according to RFC 6749
        self.request.response.cache_control = 'no-store'
        self.request.response.pragma = 'no-cache'

        return response_body


@view_defaults(containment='smartgymapi.lib.factories.oauth.OAuthFactory',
               permission='client',
               renderer='json')
class OAuthClientHandler(object):
    def __init__(self, request):
        self.request = request

    @view_config(
        context='smartgymapi.lib.factories.oauth.ClientFactory')
    def post(self):
        try:
            result, errors = OAuthClientSchema(
                strict=True,
                only=('name', 'client_type')).load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json=str(e))

        return_body = {
            "client_id": uuid.uuid4(),
            "client_secret": get_secure_token()
        }

        result.update(return_body)

        client = OAuthClient()
        client.set_fields(result)

        try:
            persist(client)
        except:
            log.critical("Something went wrong saving the client",
                         exc_info=True)
            rollback()
        finally:
            commit()

        return return_body
