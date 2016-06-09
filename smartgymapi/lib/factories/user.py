import logging

from pyramid.security import Allow, Authenticated, Everyone

from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.user import list_users, get_user

log = logging.getLogger(__name__)


class UserFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self['buddies'] = BuddyFactory(self, 'buddies')

    def __acl__(self):
        return ((Allow, Authenticated, 'user'),
                (Allow, Everyone, 'signup'))

    def __getitem__(self, key):
        if key == 'buddies':
            return BuddyFactory(self, 'buddies')

        user = get_user(key)

        if user:
            user.set_lineage(self, 'user')
            return user

        raise KeyError

    def get_users(self):
        return list_users()


class BuddyFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem(self, key):
        buddy = get_user(key)

        if buddy:
            buddy.set_lineage(self, 'user')
            return buddy

        raise KeyError

    def __acl__(self):
        return ((Allow, Authenticated, 'buddy'),)
