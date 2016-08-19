import logging

from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPCreated, HTTPNoContent
from pyramid.view import view_config, view_defaults

from smartgymapi.lib.decorators import handler_wrapper
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

    @handler_wrapper(validation_schema=SpotifySchema)
    @view_config(request_method='POST')
    def add_track(self, result):
        spotify = Spotify(
            request=self.request,
            gym=get_gym_by_MAC_address(result['client_address']))
        spotify.update_playlist()
        raise HTTPCreated

    @handler_wrapper(validation_schema=SpotifySchema)
    @view_config(request_method='DELETE')
    def delete_track(self, result):
        log.info(result)
        spotify = Spotify(
            request=self.request,
            gym=get_gym_by_MAC_address(result['client_address']))
        spotify.remove_track(uri=result['uri'])
        raise HTTPNoContent
