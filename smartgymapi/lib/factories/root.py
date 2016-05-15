from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.lib.factories.user import UserFactory
from smartgymapi.lib.factories.user_activity import UserActivityFactory


class RootFactory(dict):

    def __init__(self, request):
        self.requires_oauth = False
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['busyness'] = BusynessFactory(self, 'busyness')
        self['user'] = UserFactory(self, 'user')
        self['user_activity'] = UserActivityFactory(self, 'user_activity')
        self['sport_schedule'] = SportScheduleFactory(self, 'sport_schedule')
