from smartgymapi.lib.factories.user import UserFactory
from smartgymapi.lib.factories.user_activity import UserActivityFactory
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory


class RootFactory(dict):

    def __init__(self, request):
        self.requires_oauth = False
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['user'] = UserFactory(self, 'user')
        self['user_activity'] = UserActivityFactory(self, 'user_activity')
        self['busyness'] = UserActivityFactory(self, 'busyness')
        self['sport_schedule'] = SportScheduleFactory(self, 'sport_schedule')
