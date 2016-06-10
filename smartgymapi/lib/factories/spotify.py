import logging

from pyramid.security import Allow

from smartgymapi.lib.factories import BaseFactory

log = logging.getLogger(__name__)


class SpotifyFactory(BaseFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, 'client:confidential', 'spotify'),)
