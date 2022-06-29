import typing


class BaseStorage:
    def __init__(self):
        pass

    def get(self, k: str) -> typing.Any:
        pass

    def set(self, k: str, v: typing.Any) -> None:
        pass

    def delete(self, k: str) -> None:
        pass

    def wipe(self) -> None:
        pass

    def save(self, path: str = "") -> str:
        pass

    def load(self, path: str) -> None:
        pass
