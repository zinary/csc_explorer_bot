# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = block_details_from_dict(json.loads(json_string))

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
class Miner:
    address: str
    alias: str
    type: int

    @staticmethod
    def from_dict(obj: Any) -> 'Miner':
        assert isinstance(obj, dict)
        address = from_str(obj.get("address"))
        alias = from_str(obj.get("alias"))
        type = from_int(obj.get("type"))
        return Miner(address, alias, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = from_str(self.address)
        result["alias"] = from_str(self.alias)
        result["type"] = from_int(self.type)
        return result


@dataclass
class BlockDetails:
    data: str
    difficulty: int
    fee: int
    gas_limit: int
    gas_used: int
    hash: str
    height: int
    internal_count: int
    miner: Miner
    nonce: str
    parent_hash: str
    reward: int
    size: int
    timestamp: int
    total_difficulty: int
    total_reward: int
    tx_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'BlockDetails':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        difficulty = int(from_str(obj.get("difficulty")))
        fee = int(from_str(obj.get("fee")))
        gas_limit = from_int(obj.get("gas_limit"))
        gas_used = from_int(obj.get("gas_used"))
        hash = from_str(obj.get("hash"))
        height = from_int(obj.get("height"))
        internal_count = from_int(obj.get("internal_count"))
        miner = Miner.from_dict(obj.get("miner"))
        nonce = from_str(obj.get("nonce"))
        parent_hash = from_str(obj.get("parent_hash"))
        reward = int(from_str(obj.get("reward")))
        size = from_int(obj.get("size"))
        timestamp = from_int(obj.get("timestamp"))
        total_difficulty = int(from_str(obj.get("total_difficulty")))
        total_reward = int(from_str(obj.get("total_reward")))
        tx_count = from_int(obj.get("tx_count"))
        return BlockDetails(data, difficulty, fee, gas_limit, gas_used, hash, height, internal_count, miner, nonce, parent_hash, reward, size, timestamp, total_difficulty, total_reward, tx_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["difficulty"] = from_str(str(self.difficulty))
        result["fee"] = from_str(str(self.fee))
        result["gas_limit"] = from_int(self.gas_limit)
        result["gas_used"] = from_int(self.gas_used)
        result["hash"] = from_str(self.hash)
        result["height"] = from_int(self.height)
        result["internal_count"] = from_int(self.internal_count)
        result["miner"] = to_class(Miner, self.miner)
        result["nonce"] = from_str(self.nonce)
        result["parent_hash"] = from_str(self.parent_hash)
        result["reward"] = from_str(str(self.reward))
        result["size"] = from_int(self.size)
        result["timestamp"] = from_int(self.timestamp)
        result["total_difficulty"] = from_str(str(self.total_difficulty))
        result["total_reward"] = from_str(str(self.total_reward))
        result["tx_count"] = from_int(self.tx_count)
        return result


def block_details_from_dict(s: Any) -> BlockDetails:
    return BlockDetails.from_dict(s)


def block_details_to_dict(x: BlockDetails) -> Any:
    return to_class(BlockDetails, x)
