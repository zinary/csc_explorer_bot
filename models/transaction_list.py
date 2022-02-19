# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = transactions_from_dict(json.loads(json_string))

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
class Transactions:
    amount: int
    error: str
    fee: str
    from_address: Address
    height: int
    index: int
    method: str
    status: int
    timestamp: int
    to_address: Address
    tx_hash: str

    @staticmethod
    def from_dict(obj: Any) -> 'Transactions':
        assert isinstance(obj, dict)
        amount = float(from_str(obj.get("amount")))
        error = from_str(obj.get("error"))
        fee = from_str(obj.get("fee"))
        transactions_from = Address.from_dict(obj.get("from"))
        height = from_int(obj.get("height"))
        index = from_int(obj.get("index"))
        method = from_str(obj.get("method"))
        status = from_int(obj.get("status"))
        timestamp = from_int(obj.get("timestamp"))
        to = Address.from_dict(obj.get("to"))
        tx_hash = from_str(obj.get("tx_hash"))
        return Transactions(amount, error, fee, transactions_from, height, index, method, status, timestamp, to, tx_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_str(str(self.amount))
        result["error"] = from_str(self.error)
        result["fee"] = from_str(self.fee)
        result["from"] = to_class(Address, self.from_address)
        result["height"] = from_int(self.height)
        result["index"] = from_int(self.index)
        result["method"] = from_str(self.method)
        result["status"] = from_int(self.status)
        result["timestamp"] = from_int(self.timestamp)
        result["to"] = to_class(Address, self.to_address)
        result["tx_hash"] = from_str(self.tx_hash)
        return result


def transactions_from_dict(s: Any) -> Transactions:
    return Transactions.from_dict(s)


def transactions_to_dict(x: Transactions) -> Any:
    return to_class(Transactions, x)
