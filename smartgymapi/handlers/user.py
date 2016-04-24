import logging
from marshmallow import ValidationError
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config, view_defaults
from smartgymapi.lib.encrypt import hash_password
from smartgymapi.lib.factories.user import UserFactory
from smartgymapi.lib.validation.auth import SignupSchema
from smartgymapi.lib.validation.user import UserSchema
from smartgymapi.models import commit, persist, rollback
from smartgymapi.models.user import User

log = logging.getLogger(__name__)


@view_defaults(containment=UserFactory,
               permission='public',
               renderer='json')
class RESTUser(object):
    def __init__(self, request):
        self.request = request

    @view_config(context=UserFactory, request_method="GET")
    def list(self):
        return UserSchema(many=True).dump(self.request.context.get_users())

    @view_config(context=User, request_method="GET")
    def get(self):
        return UserSchema().dump(self.request.context)

    @view_config(context=UserFactory, request_method="POST")
    def post(self):
        try:
            result, errors = SignupSchema(strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        user = User()
        user.password_hash, user.password_salt = hash_password(
            result['password'])

        self.save(user)

    @view_config(context=User, request_method="PUT")
    def put(self):
        self.save(self.request.context)

    def save(self, user):
        try:
            result, errors = UserSchema(Strict=True).load(
                self.request.json_body)
        except ValidationError as e:
            raise HTTPBadRequest(json={'message': str(e)})

        user.set_fields(result)

        try:
            persist(user)
        except:
            log.critical("Something went wrong saving the user",
                         exc_info=True)
            rollback()
            raise HTTPInternalServerError
        finally:
            commit()
