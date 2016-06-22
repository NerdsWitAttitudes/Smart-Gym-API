import logging

from pyramid.security import Allow, Authenticated

from smartgymapi.lib.factories import BaseFactory

from smartgymapi.models.user_activity import (
    list_user_activities,
    list_user_activities_for_prediction)

log = logging.getLogger(__name__)


class BusynessFactory(BaseFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, Authenticated, 'busyness'),)

    def get_busyness(self, date, gym):
        return list_user_activities(gym, date)

    def get_predicted_busyness(self, date, gym):
        return list_user_activities_for_prediction(gym, date)
