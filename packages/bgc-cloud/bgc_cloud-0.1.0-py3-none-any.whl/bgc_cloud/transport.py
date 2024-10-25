import requests
from ._fn import Credentials


class BGCTransport:
    _PATH: str = "https://apiv2.bobgroganconsulting.com/api/v1"

    def __init__(self, action, trigger):
        self._cred: Credentials | None = None
        self._action = action
        self._trigger = trigger

    @property
    def credentials(self):
        return

    @credentials.setter
    def credentials(self, cred: Credentials):
        self._cred = cred

    def send(self, data: dict, headers=None):
        try:
            res = requests.post(
                self._PATH,
                json=data
            ).json()
            return res
        except Exception as e:
            print(e)
            return

    def _build_data(self, data):
        return {
            "action": self._action,
            "trigger": self._trigger,
            "config": vars(self._cred),
            "data": dict(data),
        }
