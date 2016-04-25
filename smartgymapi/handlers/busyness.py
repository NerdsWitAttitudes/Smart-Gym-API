import logging
from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config, view_defaults
from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.validation.busyness import BusynessSchema

log = logging.getLogger(__name__)


@view_defaults(containment=BusynessFactory,
               permission='public',
               renderer='json')
class RESTBusyness(object):

    def __init__(self, request):
        self.request = request

    @view_config(view_name='past', context=BusynessFactory,
                 request_method="GET")
    def get_past_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        past_busyness = self.request.context.get_busyness(result['date'])

    @view_config(view_name='today', context=BusynessFactory,
                 request_method="GET")
    def get_todays_busyness(self):
        todays_busyness = self.request.context.get_busyness()
        todays_predicted_busyness = self.request.context.get_busyness()

    @view_config(view_name='predict', context=BusynessFactory,
                 request_method="GET")
    def get_predicted_busyness(self):
        try:
            result, errors = BusynessSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        predicted_business = self.request.context.get_predicted_busyness(
            result['date'])
