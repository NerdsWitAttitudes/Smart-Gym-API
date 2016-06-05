import datetime
import logging
import uuid

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.encrypt import get_secure_token
from smartgymapi.lib.validation.oauth import (GETTokenSchema,
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
            result, errors = GETTokenSchema(strict=True).load(
                self.request.json_body)
            grant_type = result['grant_type']
        except ValidationError as e:
            raise HTTPBadRequest(json=str(e))

        client = self.request.context.get_client(grant_type)

        token = OAuthAccessToken()
        token.access_token = get_secure_token()
        token.client = client
        token.expire_date = (datetime.datetime.now() +
                             datetime.timedelta(hours=1))
        token.type = 'bearer'

        try:
            persist(token)
            response_body = ''
        except:
            log.critical("Something went wrong saving the token",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

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
            log.critical("Something went wrong saving the client",
                         exc_info=True)
        except:
            rollback()
        finally:
            commit()

        return return_body
