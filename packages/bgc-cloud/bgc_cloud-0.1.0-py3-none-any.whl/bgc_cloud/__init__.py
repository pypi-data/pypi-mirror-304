import dataclasses
from .auth import BGCAuth
from ._fn import (Credentials)


class BGCCloud:
    __CREDENTIALS: Credentials | None
    INSTANCE = None

    def __init__(self):
        BGCCloud.INSTANCE = self

    @classmethod
    def initialise(cls, credentials: Credentials):
        cls.__CREDENTIALS = credentials

    @property
    def credentials(self):
        return self.credentials

    @classmethod
    def auth(cls) -> BGCAuth:
        return BGCAuth(cls.credentials)
