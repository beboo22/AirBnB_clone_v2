#!/usr/bin/python3
""" Store first object """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ class FileStorage """

    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """do nothing"""
        pass

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        dictionary = {}
        for key, value in self.__objects.items():
            dictionary[key] = value.to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as f:
            json.dump(dictionary, f, indent=2)

    def reload(self):
        """
        deserializes the JSON file
        to __objects (only if the
        JSON file (__file_path)
        """
        models = {'User': User, 'BaseModel': BaseModel, 'State': State,
                  'City': City, 'Amenity': Amenity, 'Place': Place,
                  'Review': Review}
        try:
            with open(self.__file_path, "r", encoding='utf-8') as f:
                json_objs = json.load(f)

            for key, value in json_objs.items():
                for model, cls in models.items():
                    if value["__class__"] == model:
                        self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass
