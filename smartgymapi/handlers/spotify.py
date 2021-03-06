import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPCreated, HTTPNoContent
from pyramid.view import view_config, view_defaults


from smartgymapi.lib.factories.spotify import SpotifyFactory
from smartgymapi.lib.spotify.spotify import Spotify
from smartgymapi.lib.validation.spotify import SpotifySchema
from smartgymapi.models.gym import get_gym_by_MAC_address

log = logging.getLogger(__name__)


@view_defaults(containment=SpotifyFactory,
               permission='spotify',
               renderer='json',
               context=SpotifyFactory)
class RESTSpotify(object):

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    @view_config(request_method='GET', name='genres', permission='public')
    def get_genres(self):
        spotify = Spotify(self.request)
        return spotify.get_genre_seeds()

    @view_config(request_method='POST')
    def add_track(self):
        try:
            result, errors = SpotifySchema(
                strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})
        log.info(result)
        spotify = Spotify(
            self.request, get_gym_by_MAC_address(result['client_address']))
        spotify.update_playlist()
        raise HTTPCreated

    @view_config(request_method='DELETE')
    def delete_track(self):
        try:
            result, errors = SpotifySchema(
                strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})
        spotify = Spotify(
            self.request, get_gym_by_MAC_address(result['client_address']))
        spotify.remove_track(result['uri'])
        raise HTTPNoContent
