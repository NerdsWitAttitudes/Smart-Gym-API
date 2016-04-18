from smartgymapi.lib.factories.user import UserFactory


class RootFactory(dict):
    def __init__(self, request):
        self.requires_oauth = False
        self.request = request
        self.__name__ = None
        self.__parent__ = None

        self['user'] = UserFactory(self, 'user')
