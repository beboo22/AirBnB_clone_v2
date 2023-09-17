#!/usr/bin/python3
""" User model """
from models.base_model import BaseModel 
import models
from sqlalchemy import Column, Integer, String 



class User(BaseModel):
    """represent User class"""

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    __tablename__ = "users"
    