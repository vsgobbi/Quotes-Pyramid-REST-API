def includeme(config):
    config.add_route('index', '/')
    config.add_route('home', '/home')
    config.add_route('quotes', '/quotes')
    config.add_route('random_quote', '/quotes/random')
    config.add_route('get_quote', '/quotes/{id}')
    config.add_route('delete_quote', '/delete/{id}')
    config.add_route('get_sessions', '/sessions')
    config.add_route('get_session', '/sessions/{id}')
