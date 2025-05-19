#!/usr/bin/python3
"""Defines the BaseModel class."""
# from models import storage
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

Base = declarative_base()


class BaseModel(Base):
    """Defines the BaseModel class.
    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    __abstract__ = True
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.now(timezone.utc)
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"] and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)
    def save(self):
        """Update updated_at with the current datetime."""
        from models import storage
        self.updated_at = datetime.now(timezone.utc)
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage
        storage.delete(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)
