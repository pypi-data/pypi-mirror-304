from dataclasses import dataclass
from typing import Optional, TypeVar

T = TypeVar("T")


@dataclass
class PubKey:
    """
    PubKey represents a public key composed by the type and its value.
    """

    _type: str
    key: str

    @classmethod
    def from_dict(cls, data: dict) -> "PubKey":
        return cls(
            _type=data["@type"],
            key=data["key"],
        )


@dataclass
class Account:
    """
    Account represents a Cosmos SDK account.
    """

    _type: str
    address: str
    pub_key: Optional[PubKey]
    account_number: str
    sequence: str

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        account_data = data["account"]
        try:
            pub_key = PubKey.from_dict(account_data["pub_key"])

        except TypeError as e:
            pub_key = None

        return cls(
            _type=account_data["@type"],
            address=account_data["address"],
            pub_key=pub_key,
            account_number=account_data["account_number"],
            sequence=account_data["sequence"],
        )


@dataclass
class QueryAccountResponse:
    """
    QueryAccountResponse represents the response returned from the query to the
    API cosmos/auth/v1beta1/accounts/{account}.
    """

    account: Account
