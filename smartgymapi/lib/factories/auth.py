from pyramid.security import Allow, Authenticated, Everyone

from smartgymapi.lib.factories import BaseFactory


class AuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, Everyone, 'login'),
                (Allow, Authenticated, 'logout'))
