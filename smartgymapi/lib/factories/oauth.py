import logging

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.lib.validation.oauth import GETTokenSchema

log = logging.getLogger(__name__)


class OAuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['client_credentials'] = ClientCredentialsFactory(
            self,
            'client_credentials')

    def __getitem__(self, key):
        # preemptive validation stuff
        try:
            result, errors = GETTokenSchema(strict=True).load(
                self.request.GET)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        return self[grant_type]


class ClientCredentialsFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
