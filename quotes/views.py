from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from quotes.models import Quote, Session, DBSession
from sqlalchemy.exc import DBAPIError
from random import randint
import json
import transaction
import logging


@view_defaults(route_name="quotes", renderer="json")
class QuoteView(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get_quotes(self):
        try:
            results = DBSession.query(Quote).order_by(Quote.id).all()
            json_result = []
            for row in results:
                row_dict = dict(title=row.title, description=row.description, created_at=row.created_at)
                json_result.append(row_dict)
            print(json_result)
            return Response(status=200,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"quotes": json_result}))
        except DBAPIError as exec:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"error": exec.args}))

    @view_config(route_name="get_quote", renderer="json", request_method="GET")
    def get_quote(self):
        id = self.request.matchdict["id"]
        if id:
            result = DBSession.query(Quote).filter(Quote.id == id).first()
            if result:
                try:
                    result = result.to_json()
                    print(result)
                    return Response(status=200,
                                    content_type="application/json",
                                    charset="UTF-8",
                                    body=json.dumps({"quote": result}))
                except DBAPIError as exec:
                    return Response(status=400,
                                    body=json.dumps({"error": exec.args}))
        return Response(status=400,
                        content_type="application/json",
                        charset="UTF-8",
                        body=json.dumps({"error": "quote {id} not found".format(id=id)}))

    @view_config(route_name="delete_quote", renderer="json", request_method="DELETE")
    def delete_quote(self):
        id = self.request.matchdict["id"]
        if id:
            obj = DBSession.query(Quote).filter(Quote.id == id).first()
            if obj:
                try:
                    DBSession.delete(obj)
                    transaction.commit()
                    return Response(status=200,
                                    content_type="application/json",
                                    charset="UTF-8",
                                    body=json.dumps({"deleted": obj.to_dict()}))
                except DBAPIError as exec:
                    return Response(status=400,
                                    body=json.dumps({"error": exec.args}))
        else:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"error": "quote {id} not found".format(id=id)}))

    @view_config(route_name="random_quote", renderer="json", request_method="GET")
    def random_quote(self):
        try:
            rows = DBSession.query(Quote).count()
            random_id = (randint(1, rows))
            print("Picked quote:", random_id)
            result = DBSession.query(Quote).filter_by(id=random_id).first()
            return Response(status=200,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps(result.to_dict()))
        except DBAPIError as exec:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"error": exec.args}))

    @view_config(request_method="POST")
    def post_quotes(self):
        content_type = self.request.content_type
        body = self.request.body
        print(body)
        if body is None:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"error": "content not found"}))
        if content_type == "application/json":
            quotes = self.request.json
        else:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({'error': 'content type must be json'}))

        if type(quotes) is not dict or quotes.values() is None:
            json_format_error = {'error': 'malformed json, ex: {quotes: {quote1: {Flat is better than nested.}'}
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps(json_format_error))

        if len(quotes.items()) > 0:
            print("Quotes to save:", len(quotes.items()))
            try:
                for keys, values in quotes.items():
                    Quote.unpack_and_save_values(data=values)
                return Response(status=201,
                                content_type="application/json",
                                charset="UTF-8")
            except DBAPIError as exec:
                return Response(status=400,
                                content_type="application/json",
                                charset="UTF-8",
                                body=json.dumps({"error": exec.args}))
        else:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"error": "bad request"}))


@view_defaults(renderer="index.pt")
class SessionView:

    def __init__(self, request):
        self.log = logging.getLogger(__name__)
        self.request = request

    @property
    def counter(self):
        session = self.request.session
        if "counter" in session:
            session["counter"] += 1
            print(session["counter"])
            print("SAVED REGISTRY: ", session.items())
            logging.debug(session.items())
            self.create_sessions()
        else:
            session['counter'] = 1

        transaction.commit()
        return int(session['counter'])

    def create_sessions(self):
        session = self.request.session
        str_page = str(self.request.url)
        try:
            save_session = {"counter": session["counter"], "page": str_page}
            update_entity = DBSession.query(Session).filter_by(page=str_page).first()
            update_entity.counter += 1
            logging.debug("Saved session register: ", save_session)
            print("Current visited page: ", self.request.url)
            DBSession.add(update_entity)
            transaction.commit()
        except DBAPIError as exec:
            return {"internal error": {exec.args}}

    @view_config(route_name="home")
    def home(self):
        return {"name": "Home View"}

    @view_config(route_name="index")
    def index(self):
        return Response("<Title>Desafio Web 1.0</Title>")

    @view_config(route_name="get_sessions", request_method="GET", renderer="json")
    def get_sessions(self):
        try:
            results = DBSession.query(Session).order_by(Session.id).all()
            json_result = []
            print(results)
            for row in results:
                row_dict = dict(page=row.page,
                                counter=row.counter,
                                created_at=row.created_at)
                json_result.append(row_dict)
            print(json_result)
            return Response(status=200,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps({"sessions": json_result}))
        except DBAPIError as exec:
            json_db_error = {"error": exec.args}
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=json.dumps(json_db_error))

    @view_config(route_name="get_session", request_method="GET", renderer="json")
    def get_session(self):
        id = self.request.matchdict["id"]
        if id:
            result = DBSession.query(Session).filter(Session.id == id).first()
            if result:
                try:
                    return Response(status=200,
                                    content_type="application/json",
                                    charset="UTF-8",
                                    body=json.dumps(result.to_dict()))
                except DBAPIError as exec:
                    json_db_error = {"error": exec.args}
                    return Response(status=400,
                                    content_type="application/json",
                                    charset="UTF-8",
                                    body=json.dumps(json_db_error))
        return Response(status=400,
                        content_type="application/json",
                        charset="UTF-8",
                        body=json.dumps({"error": "session not found"}))
