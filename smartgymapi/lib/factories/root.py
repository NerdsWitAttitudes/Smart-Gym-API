
from smartgymapi.lib.factories.auth import AuthFactory
from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.factories.device import DeviceFactory
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.lib.factories.user import UserFactory
from smartgymapi.lib.factories.user_activity import UserActivityFactory

from pyramid.security import Allow, Everyone


class RootFactory(dict):

    def __init__(self, request):
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['busyness'] = BusynessFactory(self, 'busyness')
        self['user'] = UserFactory(self, 'user')
        self['user_activity'] = UserActivityFactory(self, 'user_activity')
        self['auth'] = AuthFactory(self, 'auth')
        self['device'] = DeviceFactory(self, 'device')
        self['sport_schedule'] = SportScheduleFactory(self, 'sport_schedule')

    def __acl__(self):
        return ((Allow, Everyone, 'public'),)
