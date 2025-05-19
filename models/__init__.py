from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage_tempo import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
