from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.city import City
from sqlalchemy.orm import relationship
from os import getenv
import models

class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        @property
        def cities(self):
            """Returns the list of City instances with state_id equal to current State.id"""
            return [city for city in models.storage.all(City).values() if city.state_id == self.id]
