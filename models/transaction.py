# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = transaction_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast

from models.address import Address

T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Method:
    verified: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Method':
        assert isinstance(obj, dict)
        verified = from_bool(obj.get("verified"))
        return Method(verified)

    def to_dict(self) -> dict:
        result: dict = {}
        result["verified"] = from_bool(self.verified)
        return result



@dataclass
class Transaction:
    data: str
    error: str
    fee: str
    fee_usd: str
    from_address: Address
    gas_limit: int
    gas_price: str
    gas_used: int
    height: int
    index: int
    method: Method
    nonce: int
    status: int
    timestamp: int
    to_address: Address
    transfers: List[Any]
    tx_hash: str
    value: str
    value_usd: str

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        error = from_str(obj.get("error"))
        fee = from_str(obj.get("fee"))
        fee_usd = from_str(obj.get("fee_usd"))
        transaction_from = Address.from_dict(obj.get("from"))
        gas_limit = from_int(obj.get("gas_limit"))
        gas_price = from_str(obj.get("gas_price"))
        gas_used = from_int(obj.get("gas_used"))
        height = from_int(obj.get("height"))
        index = from_int(obj.get("index"))
        method = Method.from_dict(obj.get("method"))
        nonce = from_int(obj.get("nonce"))
        status = from_int(obj.get("status"))
        timestamp = from_int(obj.get("timestamp"))
        to = Address.from_dict(obj.get("to"))
        transfers = obj.get("transfers")
        tx_hash = from_str(obj.get("tx_hash"))
        value = (from_str(obj.get("value")))
        value_usd = from_str(obj.get("value_usd"))
        return Transaction(data, error, fee, fee_usd, transaction_from, gas_limit, gas_price, gas_used, height, index, method, nonce, status, timestamp, to, transfers, tx_hash, value, value_usd)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["error"] = from_str(self.error)
        result["fee"] = from_str(self.fee)
        result["fee_usd"] = from_str(self.fee_usd)
        result["from"] = to_class(Address, self.from_address)
        result["gas_limit"] = from_int(self.gas_limit)
        result["gas_price"] = from_str(self.gas_price)
        result["gas_used"] = from_int(self.gas_used)
        result["height"] = from_int(self.height)
        result["index"] = from_int(self.index)
        result["method"] = to_class(Method, self.method)
        result["nonce"] = from_int(self.nonce)
        result["status"] = from_int(self.status)
        result["timestamp"] = from_int(self.timestamp)
        result["to"] = to_class(Address, self.to_address)
        result["transfers"] = self.transfers
        result["tx_hash"] = from_str(self.tx_hash)
        result["value"] = from_str(str(self.value))
        result["value_usd"] = from_str(self.value_usd)
        return result


def transaction_from_dict(s: Any) -> Transaction:
    return Transaction.from_dict(s)


def transaction_to_dict(x: Transaction) -> Any:
    return to_class(Transaction, x)
