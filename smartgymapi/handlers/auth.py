import datetime
import logging
from functools import partial
from marshmallow import ValidationError
from pyramid.view import view_config
from pyramid.security import forget, remember
from pyramid.httpexceptions import HTTPBadRequest
from sqlalchemy.orm.exc import NoResultFound
from smartgymapi.lib.factories.auth import AuthFactory
from smartgymapi.lib.validation.auth import LoginSchema
from smartgymapi.lib.encrypt import check_password
from smartgymapi.models import persist, commit, rollback
from smartgymapi.models.user import get_user_by_email

log = logging.getLogger(__name__)

auth_factory_view = partial(
    view_config,
    context=AuthFactory,
    renderer='json'
)


@auth_factory_view(permission='login',
                   request_method='POST', name='login')
def login(request):
    _logout(request)
    schema = LoginSchema(strict=True)

    try:
        result, errors = schema.load(request.POST)
    except ValidationError as e:
        raise HTTPBadRequest(json={'message': str(e)})

    try:
        user = get_user_by_email(email=result['email'])
    except NoResultFound:
        raise HTTPBadRequest(
            json={"message": "User and password don't match"})

    check_password(result['password'], user.password_hash, user.password_salt)

    remember(request, user.id)
    user.last_login = datetime.datetime.now()
    try:
        persist(user)
    except:
        # We do not cancel the log in since this should not affect the user
        log.critical("Something went wrong logging in the user", exc_info=True)
        rollback()
    finally:
        commit()


@auth_factory_view(request_method='GET', name='logout')
def logout(request):
    _logout(request)


def _logout(request):
    request.session.invalidate()
    forget(request)
