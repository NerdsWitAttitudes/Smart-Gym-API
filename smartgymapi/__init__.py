import logging

import threading
import spotify


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

log = logging.getLogger(__name__)


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
    config.scan('smartgymapi.handlers')

    # spotify
    spotify_config = spotify.Config()
    spotify_config.user_agent = 'Spotify client'
    spotify_session = spotify.Session(spotify_config)
    logged_in_event = threading.Event()

    def connection_state_listener(session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in_event.set()

    spotify_session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED,
        connection_state_listener)
    spotify_session.login(
        settings['spotify.username'], settings['spotify.password'])
    while not logged_in_event.wait(0.1):
        spotify_session.process_events()
    return config.make_wsgi_app()
