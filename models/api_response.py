# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = api_response_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class APIResponse:
    code: int
    data: dict
    message: str

    @staticmethod
    def from_dict(obj: Any) -> 'APIResponse':
        assert isinstance(obj, dict)
        code = from_int(obj.get("code"))
        data = obj.get("data")
        message = from_str(obj.get("message"))
        return APIResponse(code, data, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_int(self.code)
        result["data"] = dict(self.data)
        result["message"] = from_str(self.message)
        return result


def api_response_from_dict(s: Any) -> APIResponse:
    return APIResponse.from_dict(s)


def api_response_to_dict(x: APIResponse) -> Any:
    return to_class(APIResponse, x)
