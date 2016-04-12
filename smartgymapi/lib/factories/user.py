from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.user import list_users


class UserFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        raise KeyError()

    def get_users():
        return list_users()
