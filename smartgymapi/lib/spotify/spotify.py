import base64
import json
import logging
import requests

from smartgymapi.models import commit, persist, rollback
from smartgymapi.models.user import list_current_users_in_gym

log = logging.getLogger(__name__)


class Spotify(object):

    def __init__(self, request, gym):
        self.request = request
        self.gym = gym
        self.settings = request.registry.settings
        self.access_token = self.get_access_token()
        self.post_headers = {"Content-Type": "application/json",
                             "Authorization":
                             "Bearer {}".format(self.access_token)}
        self.get_headers = {
            "Authorization": "Bearer {}".format(self.access_token)}

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
        """
        This function gets an acces token which we need to send requests to
        the spotify API.
        """

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

        if not self.gym.spotify_playlist_id:
            # this means the playlist does not exist yet.
            # so we have to create it
            r = requests.post(
                '{}/users/{}/playlists'.format(
                    self.settings['spotify.base_url'],
                    self.settings['spotify.user_id']),
                headers=self.post_headers,
                data=json.dumps({"name": str(self.gym.id)}))

            self.gym.spotify_playlist_id = r.json()['id']

        r = requests.get('{}/users/{}/playlists/{}'.format(
            self.settings['spotify.base_url'],
            self.settings['spotify.user_id'], self.gym.spotify_playlist_id),
            headers=self.get_headers)

        params = {'seed_genres': ['dance', 'electro'], 'limit': 5}

        r = requests.get('{}/recommendations'.format(
            self.settings['spotify.base_url']), headers=self.get_headers,
            params=params)

        song_uris = []
        for song in r.json()['tracks']:
            song_uris.append(song['uri'])

        # - add numbers to playlist
        r = requests.post('{}/users/{}/playlists/{}/tracks'.format(
            self.settings['spotify.base_url'],
            self.settings['spotify.user_id'],
            self.gym.spotify_playlist_id),
            headers=self.post_headers, data=json.dumps({'uris': song_uris}))

        return
