#!/usr/bin/python3
"""Defines the Amenity class."""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import String, Table
from sqlalchemy.orm import relationship
# from models.place_amenity import PlaceAmenity


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel, Base):
    """Represents an Amenity for a MySQL database."""
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    # DO NOT use back_populates here to avoid circular reference issues
    # Use backref instead or delay evaluation with a string
    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )




