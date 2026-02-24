from .database import create_db

def run():
    create_db()
    print("QVCS repository initialized")
    