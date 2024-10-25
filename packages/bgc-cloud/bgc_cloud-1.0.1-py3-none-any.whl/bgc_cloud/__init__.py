import dataclasses
from .auth import BGCAuth
from ._fn import (Credentials)


class BGCCloud:
    __CREDENTIALS: Credentials | None = None
    INSTANCE = None

    def __init__(self):
        ...

    @classmethod
    def initialise(cls, credentials: Credentials):
        cls.__CREDENTIALS = credentials
        cls.INSTANCE = BGCCloud()

    @property
    def credentials(self):
        return self.__CREDENTIALS

    @classmethod
    def auth(cls) -> BGCAuth:
        if not cls.INSTANCE:
            raise Exception("BGCCloud is not initialised")

        return BGCAuth(cls.__CREDENTIALS)
