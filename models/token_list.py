# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = token_list_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class TokenList:
    contract: str
    create_timestamp: int
    decimals: int
    holder_count: int
    name: str
    star: bool
    symbol: str
    total_supply: str
    tx_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'TokenList':
        assert isinstance(obj, dict)
        contract = from_str(obj.get("contract"))
        create_timestamp = from_int(obj.get("create_timestamp"))
        decimals = from_int(obj.get("decimals"))
        holder_count = from_int(obj.get("holder_count"))
        name = from_str(obj.get("name"))
        star = from_bool(obj.get("star"))
        symbol = from_str(obj.get("symbol"))
        total_supply = from_str(obj.get("total_supply"))
        tx_count = from_int(obj.get("tx_count"))
        return TokenList(contract, create_timestamp, decimals, holder_count, name, star, symbol, total_supply, tx_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["contract"] = from_str(self.contract)
        result["create_timestamp"] = from_int(self.create_timestamp)
        result["decimals"] = from_int(self.decimals)
        result["holder_count"] = from_int(self.holder_count)
        result["name"] = from_str(self.name)
        result["star"] = from_bool(self.star)
        result["symbol"] = from_str(self.symbol)
        result["total_supply"] = from_str(self.total_supply)
        result["tx_count"] = from_int(self.tx_count)
        return result


def token_list_from_dict(s: Any) -> TokenList:
    return TokenList.from_dict(s)


def token_list_to_dict(x: TokenList) -> Any:
    return to_class(TokenList, x)
