from dataclasses import dataclass
from typing import List

from mantrapy.types.cosmossdk.coin import Coin
from mantrapy.types.cosmossdk.coin import Coins


@dataclass
class DelegationDelegatorReward:
    """ """

    validator_address: str
    reward: Coins

    @classmethod
    def from_dict(cls, data: dict) -> 'DelegationDelegatorReward':

        coins = Coins([Coin.from_dict(coin) for coin in data['reward']])
        return cls(validator_address=data['validator_address'], reward=coins)


@dataclass
class Rewards(List[DelegationDelegatorReward]):
    """ """

    def __init__(self, *args):
        super().__init__(*args)


@dataclass
class QueryDelegationTotalRewardsResponse:
    """ """

    rewards: Rewards
    total: Coins

    @classmethod
    def from_dict(cls, data: dict) -> 'QueryDelegationTotalRewardsResponse':

        # TODO: should be decimal coins
        coins = Coins([Coin.from_dict(coin) for coin in data['total']])
        rewards = Rewards(
            [
                DelegationDelegatorReward.from_dict(delegation)
                for delegation in data['rewards']
            ],
        )
        return cls(rewards=rewards, total=coins)
