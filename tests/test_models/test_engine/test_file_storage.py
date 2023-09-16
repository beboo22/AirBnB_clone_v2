#!/usr/bin/python3
""" Test File Storage """
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
from datetime import datetime


class TestConstructor(unittest.TestCase):
    """ test class """

    def test_default_values(self):
        """ test default value """
        initial_count = len(self.FileStorage().all())
        old_dict = self.FileStorage().all().copy()
        new_base_model = BaseModel()
        self.FileStorage().new(new_base_model)
        self.FileStorage().save()
        self.FileStorage().reload()
        updated_count = len(self.FileStorage().all())
        self.assertEqual(updated_count, initial_count + 1)
        obj_key = f"BaseModel.{new_base_model.id}"
        self.assertIn(obj_key, self.FileStorage().all())
        reloaded_obj = self.FileStorage().all()[obj_key]
        self.assertEqual(reloaded_obj.updated_at, new_base_m)
