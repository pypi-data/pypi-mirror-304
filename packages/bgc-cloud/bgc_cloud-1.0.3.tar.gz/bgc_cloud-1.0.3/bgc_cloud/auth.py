from .controller import BaseController


class BGCAuth(BaseController):
    def create_user_with_email_and_password(self, email, password, **kwargs):
        return self._submit(
            "auth",
            "create_user_with_email_and_password", **{
                "email": email, "password": password,
                **kwargs
            })

    def create_user_with_phone_and_password(self, phone, password, **kwargs):
        return self._submit(
            "auth",
            "create_user_with_email_and_password", **{
                "phone": phone, "password": password,
                **kwargs
            })

    def login_with_phone_and_password(self, phone, password, **kwargs):
        return self._submit(
            "auth",
            "login_with_phone_and_password", **{
                "phone": phone, "password": password,
                **kwargs
            })

    def login_with_email_and_password(self, email, password, **kwargs):
        return self._submit(
            "auth",
            "login_with_phone_and_password", **{
                "email": email, "password": password,
                **kwargs
            })
