from smartgymapi.lib.factories import BaseFactory


class UserFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        raise KeyError()
