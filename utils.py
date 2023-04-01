import os


def get_new_dir():
    i = 1
    while os.path.exists(f"temp/{i}"):
        i += 1
    os.makedirs(f"temp/{i}")
    return f"temp/{i}"
