#!/usr/bin/python3

"""db storage"""

from models.base_model import Base
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base

class DBStorage():
    """database file storage system"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiation"""
        env = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query the db and return a dict:"""
        classes = (Amenity, City, Place, Review, State, User)
        objs = dict()

        if cls is None:
            for item in classes:
                query = self.__session.query(item)
                for obj in query.all():
                    object_key = '{}.{}'.format(obj.__class__.name__, obj.id)
                    objs[object_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                object_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objs[object_key] = obj
        return objs

    def new(self, obj):
        """add a new object to db"""
        self.__session.add(obj)

    def save(self):
        """save the changes in the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all the tables in db"""
        Base.metadata.create_all(self.__engine)

        make_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        session = scoped_session(make_session)
        self.__session = session()

    def close(self):
        """close all queries"""
        self.__session.close()
