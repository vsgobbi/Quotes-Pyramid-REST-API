from zope.sqlalchemy import register
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from quotes.models import DBSession, Base
from quotes.views import QuoteView, SessionView

from pyramid.session import SignedCookieSessionFactory


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        engine = engine_from_config(settings, "sqlalchemy.")
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine

        config.include("pyramid_jinja2")
        config.include(".routes")
        this_session_factory = SignedCookieSessionFactory("itsaseekreet")

        config = Configurator(settings=settings,
                              root_factory="quotes.models.Root",
                              session_factory=this_session_factory)

        config.registry.dbmaker = sessionmaker(bind=engine)
        config.add_request_method(db, reify=True)

        config.include("pyramid_chameleon")
        config.include("pyramid_jinja2")
        config.include(".routes")

        session_factory = get_session_factory(engine_from_config(settings, prefix="sqlalchemy."))
        config.add_request_method(
            lambda request: get_tm_session(session_factory, request.tm),
            "dbsession",
            reify=True
        )
        config.scan(".views")

    return config.make_wsgi_app()
