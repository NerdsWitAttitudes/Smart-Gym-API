from lib.factories import BaseFactory
from smartgymapi.models.sport_scheme import list_sport_schemes


class SportSchemeFactory(BaseFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        raise KeyError()

    def get_sport_schemes(self):
        return list_sport_schemes()
