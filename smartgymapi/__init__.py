from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import authenticated_userid

from sqlalchemy import engine_from_config
from smartgymapi.models.meta import (
    DBSession,
    Base,
)
from smartgymapi.lib.encrypt import decrypt_secret
from smartgymapi.lib.factories.root import RootFactory
from smartgymapi.models.user import get_user


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy(
        secret=decrypt_secret(settings['auth.secret'],
                              settings['aes.key'],
                              settings['aes.iv']),
        timeout=settings['auth.timeout'],
        reissue_time=settings['auth.reissue_time'],
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
    return config.make_wsgi_app()
