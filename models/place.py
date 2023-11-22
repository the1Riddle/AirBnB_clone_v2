#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import models
from os import getenv


place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night =  Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)

    @property
    def reviews(self):
        """getter attribute returns the list of Review instances"""
        if env.HBNB_TYPE_STORAGE == 'db':
            return self.__reviews

        from models import storage
        from models.review import Review
        review_list = []
        for rev in storage.all(Review).values():
            if rev.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """getter attribute returns the list of Amenity instances"""
        if env.HBNB_TYPE_STORAGE == 'db':
            return self.__amenities

        from models import storage
        from models.amenity import Amenity
        amenity_list = []
        for amen in storage.all(Amenity).values():
            if amen.place_id in self.amenity_ids:
                amenity_list.append(amen)
        return amenity_list
