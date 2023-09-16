#!/usr/bin/python3
""" all common attributes/methods for other classes """
import uuid
from datetime import datetime
import models


class BaseModel:
    """ Base Model Class """
    def __init__(self, *args, **kwargs):
        """ initialize the function """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "updated_at":
                        self.updated_at = datetime.fromisoformat(value)
                    elif key == "created_at":
                        self.created_at = datetime.fromisoformat(value)
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """ return string """
        return f"[{self.__class__.__name__}] ({self.id}) <{self.__dict__}>"

    def save(self):
        """ updates the public instance attribute """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing
        all keys/values of __dict__ of the instance
        """
        my_obj_dict = self.__dict__.copy()
        my_obj_dict["__class__"] = self.__class__.__name__
        my_obj_dict["created_at"] = self.created_at.isoformat()
        my_obj_dict["updated_at"] = self.updated_at.isoformat()
        return my_obj_dict
