from ._fn import Credentials
from .transport import BGCTransport


class BGCAuth:
    def __init__(self, cred: Credentials):
        self.cred = cred

    def create_user_with_email_and_password(self, email, password, **kwargs):
        res = self._submit(
            "auth",
            "create_user_with_email_and_password", **{
                "email": email, "password": password,
                **kwargs
            })
        if res:
            print(res)
            return res

    def _submit(self, action, trigger, **data):
        transport = BGCTransport(action, trigger)
        transport.credentials = self.cred
        return transport.send(data)
