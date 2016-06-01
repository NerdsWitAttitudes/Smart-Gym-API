import logging

from pyramid.security import Allow, Authenticated

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.cardio_activity import get_cardio_activity, list_cardio_activities, is_cardio_activity_active

log = logging.getLogger(__name__)


class CardioActivityFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        cardio_activity = get_cardio_activity(key)

        if cardio_activity:
            cardio_activity.set_lineage(self, 'cardio_activity')
            return cardio_activity

        raise KeyError()

    def list_cardio_activities(self, activity_id):
        return list_cardio_activities(activity_id)

    def is_cardio_activity_active(self, activity_id):
        return is_cardio_activity_active(activity_id)

    def __acl__(self):
        return ((Allow, Authenticated, 'cardio_activity'),)
