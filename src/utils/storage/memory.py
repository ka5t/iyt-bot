import os
import pickle
import tempfile
import typing
from utils.storage.base import BaseStorage


class NaiveStorage(BaseStorage):
    def __init__(self):
        self.storage = {}

    def get(self, k: str) -> typing.Any:
        return self.storage[k]

    def set(self, k: str, v: typing.Any) -> None:
        self.storage[k] = v

    def delete(self, k: str) -> None:
        try:
            del self.storage[k]
        except KeyError:
            pass

    def wipe(self) -> None:
        self.storage = {}

    def save(self, path: str = os.getenv("BOT_STORAGE_LOCATION", "")) -> str:
        if path == "":
            _, path = tempfile.mkstemp()

        with open(path, "wb") as f:
            pickle.dump(self.storage, f)
        return path

    def load(self, path: str = os.getenv("BOT_STORAGE_LOCATION", "")) -> None:
        with open(path, "rb") as f:
            self.storage = pickle.load(f)
