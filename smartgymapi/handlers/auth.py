import datetime
import logging
from functools import partial

from marshmallow import ValidationError
from pyramid.view import view_config
from pyramid.security import forget, remember
from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
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
        result, errors = schema.load(request.json_body)
    except ValidationError as e:
        raise HTTPBadRequest(json={'message': str(e)})

    try:
        user = get_user_by_email(email=result['email'])
    except NoResultFound:
        raise HTTPBadRequest(
            json={"message": "Email address and password don't match"})

    check_password(result['password'], user.password_hash, user.password_salt)

    headers = remember(request, str(user.id))
    user.last_login = datetime.datetime.now()
    try:
        persist(user)
    except:
        log.critical("something went wrong updating the user login date",
                     exc_info=True)
        rollback()
    finally:
        commit()

    # Continue logging in the user. Being unable to update the login date
    # should not prevent the user from logging in.
    request.response.headerlist.extend(headers)


@auth_factory_view(request_method='GET', name='logout')
def logout(request):
    _logout(request)


def _logout(request):
    request.session.invalidate()
    forget(request)
