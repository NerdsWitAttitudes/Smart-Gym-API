import json
import logging
import random

import requests
from pyramid.httpexceptions import HTTPBadRequest

from smartgymapi.models.user import list_users_in_gym
from smartgymapi.models.music_preference import list_music_preferences_for_users_in_gym

log = logging.getLogger(__name__)


class Spotify(object):

    def __init__(self, request, gym=None):
        self.request = request
        if gym:
            self.gym = gym
        self.settings = request.registry.settings
        self.access_token = self.get_access_token()
        self.post_headers = {"Content-Type": "application/json",
                             "Authorization":
                             "Bearer {}".format(self.access_token)}
        self.get_headers = {
            "Authorization": "Bearer {}".format(self.access_token)}

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
        """
        This function updates the spotify playlist with music based on the
        users currently in the gym
        """
        if not self.gym.spotify_playlist_id:
            # this means the playlist does not exist yet.
            # so we have to create it

            r = requests.post(
                '{}/users/{}/playlists'.format(
                    self.settings['spotify.base_url'],
                    self.settings['spotify.user_id']),
                headers=self.post_headers,
                data=json.dumps({"name": str(self.gym.id)}))

            if r.status_code is requests.codes.ok:
                self.gym.spotify_playlist_id = r.json()['id']
            else:
                raise HTTPBadRequest(json={'message':
                                           'something went wrong \
                                            creating the playlist'})

        tracks = self.get_tracks(self.get_genres())
        self.add_tracks_to_playlist(tracks)

    def get_genres(self):
        """this function returns 5 genres based on the users in the gym"""
        users_in_gym = list_users_in_gym(self.gym.id)

        # we have to make a list of id's because we can't use sqlalchemy's
        # in_() function with relationships. (not implemented yet)
        user_ids = []
        for user in users_in_gym:
            user_ids.append(user.id)

        genres = (
            [r.genre for r in
             list_music_preferences_for_users_in_gym(user_ids)])

        random_genres = []
        try:
            # we can only send 5 genres to spotify to give us recommendations
            for i in range(0, 5):
                random_genres.append(random.choice(genres))
        except IndexError:
            # we just return dance, Which does not matter because
            # there are no users in the gym or the users in the gym did not
            # give a music preference. so they have to deal with dance
            random_genres = ['dance']
        return random_genres

    def get_tracks(self, genres):
        """this function get tracks based on genres"""
        params = {'seed_genres': genres,
                  'limit': 1}
        r = requests.get('{}/recommendations'.format(
            self.settings['spotify.base_url']), headers=self.get_headers,
            params=params)
        song_uris = []

        if r.status_code is requests.codes.ok:
            for track in r.json()['tracks']:
                song_uris.append(track['uri'])
        return song_uris

    def remove_track(self, uri):
        """This function removes a track from the playlist"""
        requests.delete('{}/users/{}/playlists/{}/tracks'.format(
            self.settings['spotify.base_url'],
            self.settings['spotify.user_id'],
            self.gym.spotify_playlist_id),
            headers=self.post_headers,
            data=json.dumps({'tracks':
                             [{'uri': uri}]}))

    def add_tracks_to_playlist(self, tracks):
        requests.post('{}/users/{}/playlists/{}/tracks'.format(
            self.settings['spotify.base_url'],
            self.settings['spotify.user_id'],
            self.gym.spotify_playlist_id),
            headers=self.post_headers, data=json.dumps({'uris': tracks}))

    def get_genre_seeds(self):
        return requests.get('{}/recommendations/available-genre-seeds'.format(
            self.settings['spotify.base_url']),
            headers=self.get_headers).json()
