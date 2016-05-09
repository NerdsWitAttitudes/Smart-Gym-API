from smartgymapi.lib.factories.auth import AuthFactory
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.lib.factories.user import UserFactory


class RootFactory(dict):
    def __init__(self, request):
        self.requires_oauth = False
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['auth'] = AuthFactory(self, 'auth')
        self['sport_schedule'] = SportScheduleFactory(self, 'sport_schedule')
        self['user'] = UserFactory(self, 'user')
