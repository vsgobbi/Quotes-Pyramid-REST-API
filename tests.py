import unittest
import transaction
import requests
from pyramid import testing
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from quotes.models import DBSession, Base, Quote
from quotes.views import QuoteView, SessionView
from random import randint


class TestSqlAlchemy(unittest.TestCase):

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_initDb(self):
        self.config = testing.setUp()

        with transaction.manager:
            model = Quote(title="quoteTest",
                          description="Quality is never an accident;"
                                      " it is always the result of intelligent effort.",
                          created_at=None)
            DBSession.add(model)
            DBSession.flush()
            quote_id = DBSession.query(Quote).first().to_json()
            json_quote = DBSession.query(Quote).filter_by(id="1").first().to_dict()
            description = DBSession.query(Quote.description).order_by(Quote.created_at).first()
        print(quote_id)
        print(json_quote)
        print(description)

    def test_create_and_populateDB(self):
        self.config = testing.setUp()
        with transaction.manager:
            try:
                DBSession.add(Quote(title="quote_teste1",
                                description="If you don’t like unit testing your product,"
                                            " most likely your customers won’t like to test it either.",
                                created_at=None))
                DBSession.add(Quote(title="quote_teste2",
                                description="Software testing proves the existence of bugs not their absence.",
                                created_at=None))
                DBSession.flush()
            except DBAPIError as exec:
                print("SQLAlchemy Error:", exec.args)

    def test_populate_and_queryDB(self):
        self.config = testing.setUp()
        with transaction.manager:
            added_quote1 = Quote(title="quote_teste3",
                                 description="“All code is guilty, until proven innocent.”",
                                 created_at=None
                                 )
            added_quote2 = Quote(title="quote_teste4",
                                 description="“First, solve the problem. Then, write the code.”",
                                 created_at=None)
            DBSession.add(added_quote1)
            DBSession.add(added_quote2)
            DBSession.flush()
        result = DBSession.query(Quote).all()
        for row in result:
            row_dict = dict(title=row.title, description=row.description, created_at=row.created_at)
            print(row_dict)
            self.assertEqual(type(row_dict), dict)

    def test_deleleDb(self):
        DBSession.remove()
        testing.tearDown()

    def test_random_queryDB(self):
        DBSession.remove()
        self.config = testing.setUp()
        id = 20
        for i in range(1, 5):
            quote = Quote(title="quote_teste{0}".format(id), description="foo{0}".format(id), created_at=None)
            DBSession.add(quote)
            DBSession.flush()
            id += 1
        rows = DBSession.query(Quote).count()
        print("Number of table rows", str(rows))
        random_id = (randint(1, rows))
        print("Picked quote:", random_id)
        random_query = DBSession.query(Quote).filter_by(id=random_id).first()
        print(random_query.to_dict())
        self.assertEqual(type(random_query.to_dict()), dict)

    def test_serializeModel(self):
        DBSession.remove()
        self.config = testing.setUp()
        id = 10
        for i in range(15, 18):
            quote = Quote("quote_teste{0}".format(id), description="foo{0}".format(id), created_at=None)
            DBSession.add(quote)
            DBSession.flush()
            id += 1
        rows = DBSession.query(Quote).count()
        random_id = (randint(1, rows))
        random_json_query = DBSession.query(Quote).filter_by(id=random_id).first().to_json()
        print("Serialized: ", random_json_query)
        self.assertEqual(type(random_json_query), dict)


class TestQuotesAPI(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_index_title(self):
        request = testing.DummyRequest()
        objSession = SessionView(request=request)
        response = objSession.home()
        print(response)
        self.assertEqual(type(response), dict)

    def test_post_quote(self):  # Return created status (201)
        data = {"quotes": {"quote0": "Errors should never pass silently."}}
        print("items: ", data.items())
        content_type = "application/json"
        request = testing.DummyRequest(json=data, accept=content_type, content_type=content_type)
        view_obj = QuoteView(request)
        request.matchdict["quotes"] = data
        response = view_obj.post_quotes()
        self.assertEqual(response.status_code, 201)

    def test_post_quotes(self):  # Return created status (201)
        data = {"quotes": {"quote1": "Beautiful is better than ugly.",
                           "quote2": "Explicit is better than implicit.",
                           "quote3": "Simple is better than complex."}
                }
        content_type = "application/json"
        request = testing.DummyRequest(json=data, accept=content_type, content_type=content_type)
        view_obj = QuoteView(request)
        request.matchdict["quotes"] = data
        response = view_obj.post_quotes()
        self.assertEqual(response.status_code, 201)

    def test_post_quotes_raw(self):  # Return bad request(400) due to wrong content-type
        context = """quote1": "Beautiful is better than ugly."""
        content_type = "text/plain; charset=us-ascii"
        request = testing.DummyRequest(json=context, accept=content_type, content_type=content_type)
        view_obj = QuoteView(request)
        request.matchdict["quote"] = context
        response = view_obj.post_quotes()
        self.assertEqual(response.status_code, 400)

    def test_post_malformed_quote(self):  # Return bad request(400) due to wrong json format
        data = """{"quote0": }"""
        content_type = "application/json"
        request = testing.DummyRequest(json=data, accept=content_type, content_type=content_type)
        view_obj = QuoteView(request)
        request.matchdict["quotes"] = data
        response = view_obj.post_quotes()
        print(response.body)
        self.assertEqual(response.status_code, 400)

    def test_get_quotes(self):
        quote1 = Quote("quote111", description="somequote111", created_at=None)
        DBSession.add(quote1)
        quote2 = Quote("quote222", description="somequote222", created_at=None)
        DBSession.add(quote2)
        quote3 = Quote("quote333", description="somequote333", created_at=None)
        DBSession.add(quote3)
        DBSession.flush()

        request = testing.DummyRequest()
        view_obj = QuoteView(request=request)
        response = view_obj.get_quotes()
        self.assertEqual(response.status_code, 200)
        if "200" in str(request.response):
            return True

    def test_get_quote_id(self):
        quote1 = Quote("quote11", description="somequote11", created_at=None)
        DBSession.add(quote1)
        quote2 = Quote("quote22", description="somequote22", created_at=None)
        DBSession.add(quote2)
        DBSession.flush()
        id = 2
        request = testing.DummyRequest()
        request.matchdict["id"] = id
        view_obj = QuoteView(request)
        response_content = view_obj.get_quote()
        self.assertEqual(response_content.status_code, 200)

    def test_delete_quotes(self):
        quote = Quote("quote_test1", description="somequote", created_at=None)
        DBSession.add(quote)
        DBSession.flush()
        request = testing.DummyRequest()
        request.matchdict["id"] = 1
        view_obj = QuoteView(request)
        response = view_obj.delete_quote()
        print(response)
        print(type(response.body))
        self.assertEqual(response.status_code, 200)
        if "200" in str(request.response):
            return True


class TestSessionAPI(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)
        self.config = testing.setUp()
        self.config.include("pyramid_chameleon")

    def tearDown(self):
        testing.tearDown()

    def test_get_sessions(self):
        request = testing.DummyRequest()
        session = requests.Session()
        view_obj = SessionView(request=request)
        response = view_obj.get_sessions()
        print(session.cookies.get_dict())
        self.assertEqual(response.status_code, 200)

    def test_get_session(self):
        request = testing.DummyRequest()
        session = requests.Session()
        request.matchdict["id"] = 1
        view_obj = SessionView(request=request)
        response = view_obj.get_session()
        print(response)
        print(session.cookies.get_dict())

    def test_session_counter(self):
        request = testing.DummyRequest()
        view_obj = SessionView(request=request)
        response = view_obj.counter
        print(response)
        self.assertEqual(response, 1)
