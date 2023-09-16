#!/usr/bin/python3
""" User model """
from models.base_model import BaseModel ,Base
import models
from SQLAlchemy import column ,string 



class User(BaseModel):
    """represent User class"""

    email = column(string(128), nullable=False)
    password = column(string(128), nullable=False)
    first_name = column(string(128), nullable=True)
    last_name = column(string(128), nullable=True)
    __tablename__ = "users"
