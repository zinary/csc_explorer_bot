# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = chain_from_dict(json.loads(json_string))

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
class Chain:
    active: int
    average_time: str
    latest_height: int
    staking: str
    tx_count: int
    tx_per_second: str

    @staticmethod
    def from_dict(obj: Any) -> 'Chain':
        assert isinstance(obj, dict)
        active = from_int(obj.get("active"))
        average_time = from_str(obj.get("average_time"))
        latest_height = from_int(obj.get("latest_height"))
        staking = from_str(obj.get("staking"))
        tx_count = from_int(obj.get("tx_count"))
        tx_per_second = from_str(obj.get("tx_per_second"))
        return Chain(active, average_time, latest_height, staking, tx_count, tx_per_second)

    def to_dict(self) -> dict:
        result: dict = {"active": from_int(self.active), "average_time": from_str(self.average_time),
                        "latest_height": from_int(self.latest_height), "staking": from_str(self.staking),
                        "tx_count": from_int(self.tx_count), "tx_per_second": from_str(self.tx_per_second)}
        return result


def chain_from_dict(s: Any) -> Chain:
    return Chain.from_dict(s)


def chain_to_dict(x: Chain) -> Any:
    return to_class(Chain, x)
