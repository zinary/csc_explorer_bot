# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = address_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Address:
    address: str
    alias: str
    type: int

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        address = from_str(obj.get("address"))
        alias = from_str(obj.get("alias"))
        type = from_int(obj.get("type"))
        return Address(address, alias, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = from_str(self.address)
        result["alias"] = from_str(self.alias)
        result["type"] = from_int(self.type)
        return result


def address_from_dict(s: Any) -> Address:
    return Address.from_dict(s)


def address_to_dict(x: Address) -> Any:
    return to_class(Address, x)
