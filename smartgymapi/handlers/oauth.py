import logging

from marshmallow import ValidationError
from pyarmid.view import view_config, view_defaults

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
    def client_credentials(self):
        pass
