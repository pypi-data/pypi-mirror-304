import dataclasses


@dataclasses.dataclass
class Credentials:
    api_key: str

    @property
    def bind(self):
        return vars(self)
