import logging
from pyramid.view import view_config, view_defaults
from smartgymapi.lib.factories.user import UserFactory

log = logging.getLogger(__name__)


@view_defaults(containment=UserFactory,
               permission='public',
               renderer='json')
class RESTUser(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=UserFactory, request_method="GET")
    def list(self):
        return {}
