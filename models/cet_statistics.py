# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cet_statistics_from_dict(json.loads(json_string))

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
class CETStatistics:
    liquidity: str
    percent: str
    price: str
    timestamp: int

    @staticmethod
    def from_dict(obj: Any) -> 'CETStatistics':
        assert isinstance(obj, dict)
        liquidity = from_str(obj.get("liquidity"))
        percent = from_str(obj.get("percent"))
        price = from_str(obj.get("price"))
        timestamp = from_int(obj.get("timestamp"))
        return CETStatistics(liquidity, percent, price, timestamp)

    def to_dict(self) -> dict:
        result: dict = {"liquidity": from_str(self.liquidity), "percent": from_str(self.percent),
                        "price": from_str(self.price), "timestamp": from_int(self.timestamp)}
        return result


def cet_statistics_from_dict(s: Any) -> CETStatistics:
    return CETStatistics.from_dict(s)


def cet_statistics_to_dict(x: CETStatistics) -> Any:
    return to_class(CETStatistics, x)
