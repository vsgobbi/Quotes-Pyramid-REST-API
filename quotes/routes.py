def includeme(config):
    config.add_route('index', '/')
    config.add_route('quotes', '/quotes')
    config.add_route('quotes_random', '/quotes/random')
    config.add_route('quotes_id', 'quotes/{id}\d+')
    config.add_route('session_register', '/session/register')
    config.add_route('sessions', '/sessions/')
