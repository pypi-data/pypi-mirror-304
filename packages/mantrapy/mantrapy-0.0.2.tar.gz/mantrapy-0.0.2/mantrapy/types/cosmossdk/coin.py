from dataclasses import dataclass
from typing import List


@dataclass
class Coin:
    """
    Coin represents a Cosmos SDK coin.
    """

    denom: str
    amount: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Coin':
        return cls(
            denom=data['denom'],
            amount=data['amount'],
        )


class Coins(List[Coin]):
    """
    Coins extend the List type with the concrete custom type Coin to represent
    an array of coins.
    """

    def __init__(self, *args):
        super().__init__(*args)
