from pyramid.security import Allow, Everyone

from smartgymapi.lib.factories.auth import AuthFactory
from smartgymapi.lib.factories.busyness import BusynessFactory
from smartgymapi.lib.factories.cardio_activity import CardioActivityFactory
from smartgymapi.lib.factories.device import DeviceFactory
from smartgymapi.lib.factories.music_preference import MusicPreferenceFactory
from smartgymapi.lib.factories.oauth import OAuthFactory
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.lib.factories.spotify import SpotifyFactory
from smartgymapi.lib.factories.user import UserFactory
from smartgymapi.lib.factories.user_activity import UserActivityFactory


class RootFactory(dict):

    def __init__(self, request):
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['auth'] = AuthFactory(self, 'auth')
        self['busyness'] = BusynessFactory(self, 'busyness')
        self['cardio_activity'] = CardioActivityFactory(
            self, 'cardio_activity')
        self['device'] = DeviceFactory(self, 'device')
        self['music_preference'] = MusicPreferenceFactory(
            self, 'music_preference')
        self['oauth'] = OAuthFactory(self, 'oauth')
        self['sport_schedule'] = SportScheduleFactory(self, 'sport_schedule')
        self['spotify'] = SpotifyFactory(self, 'spotify')
        self['user'] = UserFactory(self, 'user')
        self['user_activity'] = UserActivityFactory(self, 'user_activity')

    def __acl__(self):
        return ((Allow, Everyone, 'public'),)
