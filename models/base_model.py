from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()

class BaseModel:
    """Base class for all models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if key != "__class__":
                    setattr(self, key, val)
            if "id" not in kwargs:
                self.id = str(uuid4())
            if "created_at" in kwargs and isinstance(self.created_at, str):
                self.created_at = datetime.fromisoformat(kwargs["created_at"])
            if "updated_at" in kwargs and isinstance(self.updated_at, str):
                self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def save(self):
        """Updates updated_at and saves to storage"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dict representation of the instance"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
