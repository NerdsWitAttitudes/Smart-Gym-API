from lib.factories import BaseFactory
from smartgymapi.models.sport_schedule import list_sport_schedules


class SportScheduleFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        raise KeyError()

    def get_sport_schedules(self):
        return list_sport_schedules()
