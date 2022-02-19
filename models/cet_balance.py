# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cet_balance_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast

from models.address import Address

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
class CETBalance:
    address: Address
    balance: str

    @staticmethod
    def from_dict(obj: Any) -> 'CETBalance':
        assert isinstance(obj, dict)
        address = Address.from_dict(obj.get("address"))
        balance = from_str(obj.get("balance"))
        return CETBalance(address, balance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = to_class(Address, self.address)
        result["balance"] = from_str(self.balance)
        return result


def cet_balance_from_dict(s: Any) -> CETBalance:
    return CETBalance.from_dict(s)


def cet_balance_to_dict(x: CETBalance) -> Any:
    return to_class(CETBalance, x)
