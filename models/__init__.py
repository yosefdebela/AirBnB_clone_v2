from dotenv import load_dotenv
from os import getenv

import os

load_dotenv() # Adjust path if necessary

# Debugging prints
print(f"HBNB_TYPE_STORAGE before check: {getenv('HBNB_TYPE_STORAGE')}")

if getenv("HBNB_TYPE_STORAGE") == "db":
    print("Using DBStorage path")
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    print("Using FileStorage path")
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
print(f"Storage object instantiated: {storage}")