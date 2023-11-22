#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.city import City
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = column(string(128), nullable=False)
    cities = relationship("City", backref='state',
                          cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """returns list of city instances"""
        from models import storage
        rel_cities = []

        cities = storage.all(city)
        for city in cities.values():
            if city.state_id == self.id:
                rel_cities.append(city)
        return rel_cities
