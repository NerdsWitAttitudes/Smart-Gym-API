import base64

import logging
import requests

from smartgymapi.models.user import list_current_users_in_gym

log = logging.getLogger(__name__)


class Spotify(object):

    def __init__(self, request, gym):
        self.request = request
        self.gym = gym
        self.settings = request.registry.settings
        self.access_token = self.get_access_token()

    def authorize(self):
        auth_body = {'grant_type': 'authorization_code',
                     'refresh_token':
                     self.settings['spotify.refresh_token'],
                     'code': self.settings['spotify.auth_code'],
                     'client_id': self.settings['spotify.client.id'],
                     'redirect_uri': 'http://www.partypeak.nl/'}
        r = requests.post(self.settings['spotify.authorize_url'],
                          data=auth_body)
        log.info(r.json())

    def get_access_token(self):
        auth_body = {'grant_type': 'refresh_token',
                     'refresh_token':
                     self.settings['spotify.refresh_token'],
                     'client_id': self.settings['spotify.client.id'],
                     'client_secret':
                     self.settings['spotify.client.secret']}
        r = requests.post(self.settings['spotify.authorize_url'],
                          data=auth_body)
        return r.json()['access_token']

    def update_playlist(self):
        users_in_gym = (list_current_users_in_gym(self.gym.id))

        r = requests.get('{}/users/{}/playlists/{}'.format(
            self.settings['spotify.base_url'],
            self.settings['spotify.user_id'], self.gym.id))

        if r.status_code is not requests.codes.ok:
            # this means the playlist does not exist yet.
            # so we have to create it
            headers = {"Authorization": "Bearer {}".format(self.access_token),
                       "Content-Type": "application/json"}
            data = {'name': 'test'}
            create_playlist_request = requests.post(
                '{}/users/{}/playlists'.format(
                    self.settings['spotify.base_url'],
                    self.settings['spotify.user_id']),
                headers=headers, data=data)
            log.info(create_playlist_request)

        # todo
        # - create playlist of not exist

        # - get music preferences
        # - get music based on that
        # - add numbers to playlist

        return
