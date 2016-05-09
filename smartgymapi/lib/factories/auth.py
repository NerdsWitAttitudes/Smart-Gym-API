from pyramid.security import Allow, Everyone
from partypeak.lib.factories import BaseFactory


class AuthFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, Everyone, 'login'),)
