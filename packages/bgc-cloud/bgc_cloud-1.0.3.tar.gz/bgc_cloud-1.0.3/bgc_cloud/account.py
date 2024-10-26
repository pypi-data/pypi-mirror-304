from .controller import BaseController


class BGCAccount(BaseController):
    def get_user_by(self, **kwargs):
        return self._submit(
            "account",
            "userData",
            **{
                "filter": kwargs
            })
