from dataclasses import dataclass

from mantrapy.types.cosmossdk.coin import Coin
from mantrapy.types.cosmossdk.coin import Coins
from mantrapy.types.cosmossdk.query import PageResponse


@dataclass
class QueryBalanceResponse:
    """Response containing a single balance for an account."""

    balance: Coin

    @classmethod
    def from_dict(cls, data: dict) -> 'QueryBalanceResponse':
        return cls(
            balance=Coin(
                denom=data['balances']['denom'],
                amount=data['balance']['amount'],
            ),
        )

    def to_dict(self) -> dict:
        return {
            'balance': {
                'denom': self.balance.denom,
                'amount': self.balance.amount,
            },
        }


@dataclass
class QueryAllBalancesResponse:
    """Response containing all balances for an account."""

    balances: Coins
    pagination: PageResponse

    @classmethod
    def from_dict(cls, data: dict) -> 'QueryAllBalancesResponse':
        coins = Coins(
            [
                Coin(denom=coin['denom'], amount=coin['amount'])
                for coin in data['balances']
            ],
        )

        return cls(
            balances=coins,
            pagination=PageResponse.from_dict(data['pagination']),
        )

    def to_dict(self) -> dict:
        return {
            'balances': [
                {
                    'denom': coin.denom,
                    'amount': coin.amount,
                }
                for coin in self.balances
            ],
            'pagination': self.pagination.to_dict(),
        }
