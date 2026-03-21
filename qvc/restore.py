from .database import restore_from_stage, insert_stage

def restore_entry():
    message, data = restore_from_stage()

    if message is None:
        print("Nothing to restore. Commit directory is Empty")
    else:
        print(f"Entry restored from commit directory to stage (ID: {data[0]:8})")