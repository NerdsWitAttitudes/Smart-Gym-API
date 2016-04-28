import logging
from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.sport_schedule import list_sport_schedules, get_sport_schedule

log = logging.getLogger(__name__)


class SportScheduleFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        sport_schedule = get_sport_schedule(key)

        if sport_schedule:
            sport_schedule.set_lineage(self, 'sport_schedule')
            return sport_schedule

        raise KeyError()

    def get_sport_schedules(self, user_id):
        return list_sport_schedules(user_id)
