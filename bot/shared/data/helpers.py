from bot.shared.data.constants import USERS_FILE

from pickle import load
from pickle import dump
from pickle import HIGHEST_PROTOCOL


def save_data(file: str, object: None):
    with open(file, "wb") as file:
        dump(object, file, HIGHEST_PROTOCOL)

def load_data(file: str) -> None:
    with open(file, "rb") as file:
        return load(file)