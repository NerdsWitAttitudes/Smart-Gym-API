import datetime
import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.validation.oauth import GETTokenSchema
from smartgymapi.models import commit, persist, rollback
from smartgymapi.models.oauth import OAuthAccessToken

log = logging.getLogger(__name__)


@view_defaults(containment='smartgymapi.lib.factories.oauth.OAuthFactory',
               permission='token',
               name='token',
               renderer='json')
class OAuthTokenHandler(object):
    def __init__(self, request):
        self.request = request
        self.settings = self.request.registery.settings

    @view_config(
        context='smartgymapi.lib.factories.oauth.ClientCredentialsFactory')
    def post(self):
        try:
            result, errors = GETTokenSchema(strict=True).load(
                self.request.json_body)
            grant_type = result['grant_type']
        except ValidationError as e:
            raise HTTPBadRequest(json=str(e))

        client = self.request.context.get_client(grant_type)

        token = OAuthAccessToken()
        token.client = client
        token.expire_date = (datetime.datetime.now() +
                             datetime.timedelta(hours=1))
        token.type = 'bearer'

        try:
            persist(token)
            response_body = 
        except:
            log.critical("Something went wrong saving the token",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

        return response_body
