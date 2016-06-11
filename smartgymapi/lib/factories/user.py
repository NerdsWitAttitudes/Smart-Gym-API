import logging
import uuid

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

        try:
            converted_key = uuid.UUID(key)
        except (TypeError, ValueError):
            raise KeyError("Invalid UUID")

        user = get_user(converted_key)

        if user:
            user.set_lineage(self, 'user')
            return user

        raise KeyError

    def get_users(self, **kwargs):
        return list_users(**kwargs)


class BuddyFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        try:
            converted_key = uuid.UUID(key)
        except (TypeError, ValueError):
            raise KeyError("Invalid UUID")

        buddy = get_user(converted_key)

        if buddy:
            buddy.set_lineage(self, 'user')
            return buddy

        raise KeyError

    def __acl__(self):
        return ((Allow, Authenticated, 'buddy'),)
