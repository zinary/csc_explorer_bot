# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = token_by_address_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class TokenInfo:
    contract: str
    name: str
    symbol: str

    @staticmethod
    def from_dict(obj: Any) -> 'TokenInfo':
        assert isinstance(obj, dict)
        contract = from_str(obj.get("contract"))
        name = from_str(obj.get("name"))
        symbol = from_str(obj.get("symbol"))
        return TokenInfo(contract, name, symbol)

    def to_dict(self) -> dict:
        result: dict = {}
        result["contract"] = from_str(self.contract)
        result["name"] = from_str(self.name)
        result["symbol"] = from_str(self.symbol)
        return result


@dataclass
class CRC:
    balance: str
    token_info: TokenInfo

    @staticmethod
    def from_dict(obj: Any) -> 'CRC':
        assert isinstance(obj, dict)
        balance = from_str(obj.get("balance"))
        token_info = TokenInfo.from_dict(obj.get("token_info"))
        return CRC(balance, token_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["balance"] = from_str(self.balance)
        result["token_info"] = to_class(TokenInfo, self.token_info)
        return result


@dataclass
class TokenByAddress:
    crc20: List[CRC]
    crc721: List[CRC]

    @staticmethod
    def from_dict(obj: Any) -> 'TokenByAddress':
        assert isinstance(obj, dict)
        crc20 = from_list(CRC.from_dict, obj.get("crc20"))
        crc721 = from_list(CRC.from_dict, obj.get("crc721"))
        return TokenByAddress(crc20, crc721)

    def to_dict(self) -> dict:
        result: dict = {}
        result["crc20"] = from_list(lambda x: to_class(CRC, x), self.crc20)
        result["crc721"] = from_list(lambda x: to_class(CRC, x), self.crc721)
        return result


def token_by_address_from_dict(s: Any) -> TokenByAddress:
    return TokenByAddress.from_dict(s)


def token_by_address_to_dict(x: TokenByAddress) -> Any:
    return to_class(TokenByAddress, x)
