import logging

from uuid import UUID
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.security import authenticated_userid

from sqlalchemy import engine_from_config
from smartgymapi.models.meta import (
    DBSession,
    Base,
)
from smartgymapi.lib.encrypt import decrypt_secret
from smartgymapi.lib.factories.root import RootFactory
from smartgymapi.lib.redis import RedisSession
from smartgymapi.lib.renderer import uuid_adapter
from smartgymapi.lib.security import SmartGymAuthenticationPolicy
from smartgymapi.models.user import get_user

log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    RedisSession(settings['redis.host'], settings['redis.port'],
                 settings['redis.db'], settings['redis.password'])

    authentication_policy = SmartGymAuthenticationPolicy(
        secret=decrypt_secret(settings['auth.secret'],
                              settings['aes.key'],
                              settings['aes.iv']),
        timeout=settings.get('auth.timeout', None),
        reissue_time=settings.get('auth.reissue_time', None),
        http_only=True,
        hashalg='sha512')
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=ACLAuthorizationPolicy(),
                          root_factory=RootFactory)

    def get_user_(request):
        user_id = authenticated_userid(request)
        if user_id is not None:
            return get_user(user_id)
        return None

    config.set_request_property(get_user_, 'user', reify=True)
    config.set_default_permission('admin')
    config.scan('smartgymapi.handlers')

    renderers = {'json': JSON()}
    for name, renderer in renderers.items():
        renderer.add_adapter(UUID, uuid_adapter)
        config.add_renderer(name, renderer)
    return config.make_wsgi_app()
