import logging
from datetime import datetime

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_defaults, view_config

from smartgymapi.models import persist, commit, rollback, delete
from smartgymapi.lib.factories.cardio_acitivty import CardioActivityFactory, is_cardio_activity_active
from smartgymapi.lib.validation.cardio_activity import CardioActivitySchema
from smartgymapi.models.cardio_activity import CardioActivity

log = logging.getLogger(__name__)


@view_defaults(containment=CardioActivityFactory,
               permission='cardio_activity',
               renderer='json')
class RESTCardioActivty(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=CardioActivityFactory, request_method='GET')
    def list(self):
        try:
            return CardioActivitySchema(many=True).dump(
                self.request.context.list_cardio_activities(self.request.user.active_activity)).data
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

    @view_config(context=CardioActivity, request_method='GET')
    def get(self):
        return CardioActivitySchema().dump(self.request.context).data

    @view_config(context=CardioActivityFactory, request_method='POST')
    def post(self):
        if is_cardio_activity_active(CardioActivity().activity_id):
            raise HTTPBadRequest(json={'message': 'There is another cardio_acitivty active'})

        self.save(CardioActivity())

    @view_config(context=CardioActivity, request_method='PUT')
    def put(self):
        cardio_activity = self.request.context
        if cardio_activity.end_date is None:
            cardio_activity.end_date = datetime.now()
        else:
            raise HTTPBadRequest(json={'message': 'Cardio activity is already ended'})

        self.save(cardio_activity)

    @view_config(context=CardioActivity, request_method='DELETE')
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical('Something went wrong deleting the cardio activity')
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    def save(self, cardio_activity):
        try:
            result, errors = CardioActivitySchema(strict=True).load(self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        cardio_activity.set_fields(result)

        try:
            persist(cardio_activity)
        except:
            log.critical('Something went wrong saving the cardio activity')
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
