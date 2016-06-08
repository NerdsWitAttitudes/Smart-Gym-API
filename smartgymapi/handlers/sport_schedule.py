import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_defaults, view_config

from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.lib.validation.sport_scheme import SportScheduleSchema
from smartgymapi.models import persist, rollback, commit, delete
from smartgymapi.models.sport_schedule import (SportSchedule,
                                               get_sport_schedule_by_name)

log = logging.getLogger(__name__)


@view_defaults(containment=SportScheduleFactory,
               permission='sport_schedule',
               renderer='json')
class RESTSportScheme(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=SportScheduleFactory, request_method="GET")
    def list(self):
        return SportScheduleSchema(many=True).dump(
            self.request.context.get_sport_schedules()).data

    @view_config(context=SportSchedule, request_method="GET")
    def get(self):
        return SportScheduleSchema().dump(self.request.context).data

    @view_config(context=SportScheduleFactory, request_method="POST")
    def post(self):
        try:
            if get_sport_schedule_by_name(self.request.json_body['name']):
                raise HTTPBadRequest(
                    json={'message': 'Sport schedule name already exists'})
        except KeyError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        self.save(SportSchedule())

    @view_config(context=SportSchedule, request_method="PUT")
    def put(self):
        self.save(self.request.context)

    def save(self, sport_schedule):
        try:
            result, errors = SportScheduleSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        sport_schedule.user = self.request.user
        sport_schedule.set_fields(result)

        try:
            persist(sport_schedule)
        except:
            log.critical("Something went wrong saving the sport schedule",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    @view_config(context=SportSchedule, request_method="DELETE")
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical("Something went wrong deleting the sport schedule",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
