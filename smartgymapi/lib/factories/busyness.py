import logging

from smartgymapi.lib.factories import BaseFactory

from smartgymapi.models.user_activity import (
    list_user_activities,
    list_user_activities_for_prediction)

log = logging.getLogger(__name__)


class BusynessFactory(BaseFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_busyness(self, date, group_by_hour):
        return list_user_activities(date)

    def get_predicted_busyness(self, date):
        return list_user_activities_for_prediction(date)
