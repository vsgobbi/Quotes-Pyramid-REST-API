from pyramid.view import view_config
from pyramid.response import Response
from quotes.models import Quote, DBSession
from sqlalchemy.exc import DBAPIError


@view_config(route_name="index")
def index(request):
    return Response("<Title>Desafio Web 1.0</Title>")


@view_config(route_name="session_counter", renderer="json")
def counter(request):
    session = request.session
    if 'counter' in session:
        session['counter'] += 1
    else:
        session['counter'] = 1
    return session['counter']


class QuoteView(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='quote/id')
    def quote_id(self):
        id = self.request.matchdict["id"]
        obj = DBSession.query(Quote).filter(Quote.id == id).first()
        if obj:
            return Response(status=200,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str({"quote": obj.to_dict()}))
        return Response(status=400,
                        content_type="application/json",
                        charset="UTF-8",
                        body=str({"error": "quote not found"}))

    @view_config(route_name="quotes", renderer="json")
    def quotes(self):
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
                            body=str({"quotes": json_result}))
        except DBAPIError as exec:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str({"error": exec.args}))

    @view_config(request_method="POST", context="Quotes", renderer="json")
    def quotes_post(self, **data):
        content_type = self.request.content_type
        body = self.request.body
        print(body)
        if body is None:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str({"error": "content not found"}))
        if content_type == "application/json":
            quotes = self.request.json
        else:
            content_type_error = {'error': 'content type must be json'}
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str(content_type_error))

        if type(quotes) is not dict or quotes.values() is None:
            json_format_error = {'error': 'malformed json, ex: {quotes: {quote1: {Flat is better than nested.}'}
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str(json_format_error))

        if len(quotes.items()) > 0:
            print("Quotes to save:", len(quotes.items()))
            try:
                for keys, values in quotes.items():
                    Quote.unpack_and_save_values(data=values)

                return Response(status=201,
                                content_type="application/json",
                                charset="UTF-8")

            except DBAPIError as exc:
                json_db_error = {"error": exc.args}
                return Response(status=400,
                                content_type="application/json",
                                charset="UTF-8",
                                body=json_db_error)
        else:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str({"error": "bad request"}))

    def delete(self):
        id = self.request.matchdict["id"]
        obj = DBSession.query(Quote).filter(Quote.id == id).first()
        if obj:
            print(obj.to_json())
            try:
                DBSession.delete(obj)
                return {"deleted": obj.to_dict()}
            except DBAPIError:
                jsonError = {"error": DBAPIError}
                return jsonError
        else:
            return Response(status=400,
                            content_type="application/json",
                            charset="UTF-8",
                            body=str({"error": "quote not found"}))
