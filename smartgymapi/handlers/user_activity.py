import logging
from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults
from smartgymapi.lib.factories.user_activity import UserActivityFactory
from smartgymapi.lib.validation.user_activity import UserActivitySchema
from smartgymapi.models import commit, persist, rollback
from smartgymapi.models.user_activity import UserActivity

log = logging.getLogger(__name__)


@view_defaults(containment=UserActivityFactory,
               permission='public',
               renderer='json')
class RESTUserActivity(object):

    def __init__(self, request):
        self.request = request

    @view_config(context=UserActivityFactory, request_method="GET")
    def list(self):
        return UserActivitySchema(many=True).dump(
            self.request.context.get_user_activities())

    @view_config(context=UserActivity, request_method="GET")
    def get(self):
        return UserActivitySchema().dump(self.request.context)

    @view_config(context=UserActivityFactory, request_method="POST")
    def post(self):
        self.save(UserActivity)

    def save(self, user_activity):
        try:
            result, errors = UserActivitySchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        user_activity.set_fields(result)

        try:
            persist(user_activity)
        except:
            log.critical("Something went wrong saving the user_activity",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
