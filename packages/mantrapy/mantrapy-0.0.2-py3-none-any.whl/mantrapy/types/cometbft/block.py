import base64
from dataclasses import dataclass
from hashlib import sha256


# TODO: add missing fields
@dataclass
class Header:
    chain_id: str
    height: str
    time: str
    app_hash: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Header':

        return cls(
            chain_id=data['chain_id'],
            height=data['height'],
            time=data['time'],
            app_hash=data['app_hash'],
        )


@dataclass
class Data:
    txs: list
    hash: list

    @classmethod
    def from_dict(cls, data: dict) -> 'Data':

        txs = list(data['txs'])
        _hash = [sha256(base64.b64decode(tx)).hexdigest() for tx in txs]

        return cls(
            txs=txs,
            hash=_hash,
        )


# TODO: add missing fields
@dataclass
class Block:
    header: Header
    data: Data

    @classmethod
    def from_dict(cls, d: dict) -> 'Block':

        header = Header.from_dict(d['header'])
        data = Data.from_dict(d['data'])

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
