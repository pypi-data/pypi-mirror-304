from .transport import BGCTransport
from ._fn import Credentials, build_response


class BaseController:
    def __init__(self, cred: Credentials):
        self.cred = cred

    def _submit(self, action, trigger, **data):
        transport = BGCTransport(action, trigger)
        transport.credentials = self.cred
        return build_response(transport.send(data))
