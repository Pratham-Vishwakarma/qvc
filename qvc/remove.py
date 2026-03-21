from .database import remove_from_stage, get_staged_data

def remove_entry(limit):
    length = get_staged_data()

    if len(length) != 0 and limit > len(length):
        print("Limit exceeded. Not enough entries to delete.")
    else:
        message, data = remove_from_stage(limit)

        if message is None:
            print("Nothing to remove. Stage is Empty")
        else:
            for i in range(len(data)):
                print(f"Entry removed from stage (ID: {data[i][0]:8})")