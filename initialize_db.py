import os
import sys
import transaction
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from quotes.models import DBSession, Quote, Session, Base


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        modelQuote = Quote(title='Root', description='Use Linux and avoid the Gates of Hell.', created_at=None)
        modelSession = Session(page='http://localhost:6543/home', counter='1', created_at=None)
        DBSession.add(modelQuote)
        DBSession.add(modelSession)
