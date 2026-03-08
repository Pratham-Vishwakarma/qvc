import os
from .database import create_db

def initialize():

    db_path = ".qvc/qvc.db"

    if os.path.exists(db_path):
        print("QVC repository already exists. Cannot initialize again.")
        return

    create_db()
    print("Initialized empty QVC repository")