from .database import create_db

def initialize():
    create_db()
    print("Initialized empty quantum repository in .qvc/")