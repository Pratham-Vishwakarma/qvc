from .database import create_db

def run():
    create_db()
    print("Initialized empty quantum repository in .qvc/")