import transaction
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension, mark_changed
from pyramid.security import Allow, Everyone
from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Root(object):

    __acl__ = [(Allow, Everyone, "view"),
               (Allow, "group:editors", "edit")]

    def __init__(self, request):
        pass


class Quote(Base):

    __tablename__ = "Quote"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, unique=True)
    description = Column(Text)
    created_at = Column(Text)

    def __init__(self, title, description, created_at):
        self.title = title
        self.description = description
        self.created_at = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    @classmethod
    def from_json(cls, data):
        return cls(**data, created_at=Quote.created_at)

    @classmethod
    def unpack_and_save_values(cls, data):
        for key, value in data.items():
            quote = {"title": key, "description": value}
            entity = Quote.from_json(quote)
            DBSession.add(entity)
            print("Saved entity:", entity.to_json())
        transaction.commit()
        return True

    def to_json(self):
        to_serialize = ['id', 'title', 'description', 'created_at']
        dict = {}
        for attr_name in to_serialize:
            dict[attr_name] = getattr(self, attr_name)
        return dict

    def to_dict(self):
        return {
            'quote': self.description
        }


class Session(Base):

    __tablename__ = "Session"
    id = Column(Integer, primary_key=True)
    page = Column(Text, unique=True)
    created_at = Column(Text)
    counter = Column(Integer)

    def __init__(self, page, counter, created_at):
        self.page = page
        self.counter = counter
        self.created_at = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

    @classmethod
    def from_json(cls, data):
        return cls(**data, created_at=Session.created_at)

    def to_json(self):
        to_serialize = ['id', 'page', 'counter', 'created_at']
        dict = {}
        for attr_name in to_serialize:
            dict[attr_name] = getattr(self, attr_name)
        return dict

    def to_dict(self):
        return {
            'id': self.id,
            'page': self.page,
            "counter": self.counter,
            'datetime': self.created_at
        }
