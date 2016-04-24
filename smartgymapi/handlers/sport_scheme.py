from pyramid.view import view_defaults, view_config
from lib.factories.sport_scheme_factory import SportSchemeFactory
from lib.validation.sport_scheme import SportSchemeSchema


@view_defaults(containment=SportSchemeFactory,
               permission='public',
               renderer='json')
class RESTSportScheme(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=SportSchemeSchema, request_method="GET")
    def list(self):
        SportSchemeSchema(many=True).dump(self.request.context.get_sport_schemes())
