import logging
from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults
from smartgymapi.lib.factories.music_preference import MusicPreferenceFactory
from smartgymapi.lib.validation.auth import MusicPreferenceSchema
from smartgymapi.models import commit, persist, rollback, delete
from smartgymapi.models.music_preference import MusicPreference

log = logging.getLogger(__name__)


@view_defaults(containment=MusicPreferenceFactory,
               permission='public',
               renderer='json')
class RESTMusicPreference(object):

    def __init__(self, request):
        self.request = request

    @view_config(context=MusicPreferenceFactory, request_method="GET")
    def list(self):
        return MusicPreferenceSchema(many=True).dump(
            self.request.context.get_users())

    @view_config(context=MusicPreference, request_method="GET")
    def get(self):
        return MusicPreferenceSchema().dump(self.request.context)

    @view_config(context=MusicPreferenceFactory, request_method="POST")
    def post(self):
        self.save(MusicPreference())

    @view_config(context=MusicPreference, request_method="PUT")
    def put(self):
        self.save(self.request.context)

    def save(self, user):
        try:
            result, errors = MusicPreferenceSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        music_preference.set_fields(result)

        try:
            persist(user)
        except:
            log.critical("Something went wrong saving the music_preference",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()

    @view_config(context=MusicPreference, request_method="DELETE")
    def delete(self):
        try:
            delete(self.request.context)
        except:
            log.critical("Something went wrong deleting the music preference",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
