import logging
from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.user_activity import (
    list_user_activities, get_user_activity)

log = logging.getLogger(__name__)


class UserActivityFactory(BaseFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        user_activity = get_user_activity(key)

        if user_activity:
            user_activity.set_lineage(self, 'user_activity')
            return user_activity

        raise KeyError()

    def get_user_activities(self):
        return list_user_activities()
