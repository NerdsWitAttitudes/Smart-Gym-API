from pyramid.view import view_defaults, view_config
from lib.factories.sport_schedule_factory import SportScheduleFactory
from lib.validation.sport_scheme import SportScheduleSchema


@view_defaults(containment=SportScheduleFactory,
               permission='public',
               renderer='json')
class RESTSportScheme(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=SportScheduleSchema, request_method="GET")
    def list(self):
        SportScheduleSchema(many=True).dump(self.request.context.get_sport_schedules())
