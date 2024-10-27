from dataclasses import dataclass
from datetime import datetime
from typing import List


# TODO: add missing fields
@dataclass
class Header:
    chain_id: str
    height: str
    time: datetime
    app_hash: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Header':

        return cls(
            chain_id=data['header']['chain_id'],
            height=data['header']['height'],
            time=data['header']['time'],
            app_hash=data['header']['app_hash'],
        )


@dataclass
class Data:
    txs: List[str]
    hash: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Data':

        return cls(
            txs=data['data']['txs'],
            hash=data['data']['hash'],
        )


# TODO: add missing fields
@dataclass
class Block:
    header: Header
    data: Data

    @classmethod
    def from_dict(cls, _data: dict) -> 'Block':

        header = Header.from_dict(_data)
        data = Data.from_dict(_data)

        return cls(
            header=header,
            data=data,
        )


# TODO: add missing fields
@dataclass
class BlockID:
    hash: str

    @classmethod
    def from_dict(cls, data: dict) -> 'BlockID':

        return cls(hash=data['hash'])


@dataclass
class ResultBlock:
    block_id: BlockID
    block: Block
