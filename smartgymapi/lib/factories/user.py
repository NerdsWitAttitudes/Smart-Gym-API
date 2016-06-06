import logging

from pyramid.security import Allow, Authenticated, Everyone

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.user import list_users, get_user

log = logging.getLogger(__name__)


class UserFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __acl__(self):
        return ((Allow, Authenticated, 'user'),
                (Allow, Everyone, 'signup'))

    def __getitem__(self, key):
        user = get_user(key)

        if user:
            user.set_lineage(self, 'user')
            return user

        raise KeyError()

    def get_users(self):
        return list_users()
