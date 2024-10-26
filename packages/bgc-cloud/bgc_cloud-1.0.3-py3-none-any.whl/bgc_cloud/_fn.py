import dataclasses
import typing as t


@dataclasses.dataclass
class Credentials:
    api_key: str

    @property
    def bind(self):
        return vars(self)


@dataclasses.dataclass
class BGCResponse:
    ok: bool
    message: str | None
    data: t.Any
    _extra: dict

    def __getitem__(self, item):
        return self._extra.get(item)


def build_response(data):
    res = BGCResponse(
        ok=data.get("ok"),
        message=data.get("message"),
        data=data.get("data"),
        _extra=data
    )
    return res
