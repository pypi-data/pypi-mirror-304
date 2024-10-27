from dataclasses import dataclass
from typing import List

from mantrapy.types.cosmossdk.coin import Coin
from mantrapy.types.cosmossdk.query import PageResponse


@dataclass
class Delegation:
    """
    Delegation represents an account delegation.
    """

    delegator_address: str
    validator_address: str
    shares: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Delegation':

        return cls(
            delegator_address=data['delegator_address'],
            validator_address=data['validator_address'],
            shares=data['shares'],
        )


@dataclass
class DelegationResponse:
    """
    Delegation response represents an account delegation with associated amount.
    """

    delegation: Delegation
    balance: Coin

    @classmethod
    def from_dict(cls, data: dict) -> 'DelegationResponse':

        return cls(
            delegation=Delegation.from_dict(data['delegation']),
            balance=Coin.from_dict(data['balance']),
        )


class DelegationResponses(List[DelegationResponse]):
    """
    Represents all the delegations performed by an account.
    """

    def __init__(self, *args):
        super().__init__(*args)


@dataclass
class QueryDelegatorDelegationsResponse:
    """Response containing the all the delegations of a single delegator."""

    delegation_responses: DelegationResponses
    pagination: PageResponse

    @classmethod
    def from_dict(cls, data: dict) -> 'QueryDelegatorDelegationsResponse':
        delegation_responses = DelegationResponses(
            [
                DelegationResponse.from_dict(delegation)
                for delegation in data['delegation_responses']
            ],
        )
        return cls(
            delegation_responses=delegation_responses,
            pagination=data['pagination'],
        )
