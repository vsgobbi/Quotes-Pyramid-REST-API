from waitress import serve
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def index(request):
    return Response("<Title>Desafio Web 1.0</Title>")


if __name__ == '__main__':

    with Configurator() as config:
        config.include("pyramid_jinja2")
        this_session_factory = SignedCookieSessionFactory('itsaseekreet')

        config.add_route('index', '/')
        config.add_view(index, route_name='index')
        config.include('pyramid_chameleon')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)
