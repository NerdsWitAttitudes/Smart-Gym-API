from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from smartgymapi.models.meta import (
    DBSession,
    Base,
    )
from smartgymapi.lib.encrypt import decrypt_secret
from smartgymapi.lib.factories.root import RootFactory


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
    config.set_default_permission('admin')
    config = Configurator(settings=settings, root_factory=RootFactory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan('smartgymapi.handlers')
    return config.make_wsgi_app()
