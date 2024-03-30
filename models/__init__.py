#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()

storage.reload()

__all__ = ['BaseModel', 'User', 'State', 'City', 'Amenity', 'Place', 'Review']

# Import all models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review



