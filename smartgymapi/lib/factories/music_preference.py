import logging
from smartgymapi.lib.factories import BaseFactory
from smartgymapi.models.music_preference import (list_music_preferences,
                                                 get_music_preference)

log = logging.getLogger(__name__)


class MusicPreferenceFactory(BaseFactory):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        music_preference = get_music_preference(key)

        if music_preference:
            music_preference.set_lineage(self, 'music_preference')
            return music_preference

        raise KeyError()

    def get_users(self):
        return list_music_preferences()
