from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from smartgymapi.models.meta import (
    DBSession,
    Base,
    )
from smartgymapi.lib.factories.root import RootFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, root_factory=RootFactory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan('smartgymapi.handlers')
    return config.make_wsgi_app()
