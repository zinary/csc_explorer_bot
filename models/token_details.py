# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = token_from_dict(json.loads(json_string))

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
class CreateInfo:
    creator: str
    hash: str
    timestamp: int

    @staticmethod
    def from_dict(obj: Any) -> 'CreateInfo':
        assert isinstance(obj, dict)
        creator = from_str(obj.get("creator"))
        hash = from_str(obj.get("hash"))
        timestamp = from_int(obj.get("timestamp"))
        return CreateInfo(creator, hash, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["creator"] = from_str(self.creator)
        result["hash"] = from_str(self.hash)
        result["timestamp"] = from_int(self.timestamp)
        return result


@dataclass
class Token:
    contract: str
    create_info: CreateInfo
    create_timestamp: int
    decimals: int
    holder_count: int
    name: str
    star: bool
    symbol: str
    total_supply: str
    tx_count: int
    token_type: int
    verify: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Token':
        assert isinstance(obj, dict)
        contract = from_str(obj.get("contract"))
        create_info = CreateInfo.from_dict(obj.get("create_info"))
        create_timestamp = from_int(obj.get("create_timestamp"))
        decimals = from_int(obj.get("decimals"))
        holder_count = from_int(obj.get("holder_count"))
        name = from_str(obj.get("name"))
        star = from_bool(obj.get("star"))
        symbol = from_str(obj.get("symbol"))
        total_supply = from_str(obj.get("total_supply"))
        tx_count = from_int(obj.get("tx_count"))
        token_type = from_int(obj.get("token_type"))
        verify = from_bool(obj.get("verify"))
        return Token(contract, create_info, create_timestamp, decimals, holder_count, name, star, symbol, total_supply, tx_count, token_type, verify)

    def to_dict(self) -> dict:
        result: dict = {"contract": from_str(self.contract), "create_info": to_class(CreateInfo, self.create_info),
                        "create_timestamp": from_int(self.create_timestamp), "decimals": from_int(self.decimals),
                        "holder_count": from_int(self.holder_count), "name": from_str(self.name),
                        "star": from_bool(self.star), "symbol": from_str(self.symbol),
                        "total_supply": from_str(self.total_supply), "tx_count": from_int(self.tx_count),
                        "token_type": from_int(self.token_type), "verify": from_bool(self.verify)}
        return result


def token_from_dict(s: Any) -> Token:
    return Token.from_dict(s)


def token_to_dict(x: Token) -> Any:
    return to_class(Token, x)
