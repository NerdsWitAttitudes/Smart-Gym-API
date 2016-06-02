import logging

from smartgymapi.lib.factories import BaseFactory

log = logging.getLogger(__name__)


class OAuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
