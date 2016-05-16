import logging
from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.cardio_activity import get_cardio_activity, list_cardio_activities

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

    def list_cardio_activities(self):
        return list_cardio_activities()
