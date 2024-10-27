import requests

from mantrapy.types.cometbft.block import Block, BlockID, ResultBlock
from mantrapy.types.cometbft.consensus import SyncInfo
from mantrapy.types.cometbft.tx import ResultTx
from mantrapy.types.cosmossdk.account import Account, QueryAccountResponse
from mantrapy.types.cosmossdk.bank import QueryAllBalancesResponse
from mantrapy.types.cosmossdk.distribution import QueryDelegationTotalRewardsResponse
from mantrapy.types.cosmossdk.staking import QueryDelegatorDelegationsResponse
from mantrapy.types.cosmossdk.types import QueryResponse

# TODO: should be moved to a config.
TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 1

API = "https://api.mantrachain.io"
RPC = "https://rpc.mantrachain.io"

QUERY_PATHS = {
    "account": "/cosmos/auth/v1beta1/accounts/{address}",
    "balances": "/cosmos/bank/v1beta1/balances/{address}",
    "status": "/status",
    "block_by_hash": "/block?hash={hash}",
    "block": "/block?height={height}",
    "tx": "/tx?hash={hash}",
    "delegator_delegations": "/cosmos/staking/v1beta1/delegations/{delegator_address}",
    "delegation_total_rewards": "/cosmos/distribution/v1beta1/delegators/{delegator_address}/rewards",
}

TX_PATHS = {"tx": "/cosmos/tx/v1beta1/txs"}


class Client:
    """
    Client defines a type to perform queries against the Mantra chain.
    """

    def __init__(
        self,
        api: str,
        rpc: str,
        timeout: int = TIMEOUT,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY,
    ) -> None:
        """
        Initialize the class with base API and RPC URLs.
        """
        # Cosmos SDK endpoint.
        self.api = api.rstrip("/")
        # CometBFT endpoint.
        self.rpc = rpc.rstrip("/")

        # Requests parameters.
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def create_api_url(self, path: str) -> str:
        """
        Construct a full API URL by appending the given path to the base API URL.
        """
        return self.api + path

    def create_rpc_url(self, path: str) -> str:
        """
        Construct a full RPC URL by appending the given path to the base RPC URL.
        """
        return self.rpc + path

    def _make_request(
        self, url: str, method: str = "GET", json: str = None, **kwargs
    ) -> QueryResponse:
        """
        Make HTTP request with retries and error handling.
        """

        # Repeat the request if it is failing
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    timeout=self.timeout,
                    json=json,
                    **kwargs,
                )
                data = response.json()

                return QueryResponse(
                    data=data,
                    status_code=response.status_code,
                )

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return QueryResponse(
                        error=str(e),
                        status_code=500,
                    )

        raise Exception("The request should be performed at least once.")

    # ---------------------------------------------------------------------------------------------
    # API
    # ---------------------------------------------------------------------------------------------
    def get_account(self, address: str) -> QueryResponse[QueryAccountResponse]:
        """
        Query the account associated with a particular address.
        """

        url = self.create_api_url(QUERY_PATHS["account"].format(address=address))
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:

            account = Account.from_dict(resp.data)
            return QueryResponse(
                data=QueryAccountResponse(account=account),
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_balances(self, address: str) -> QueryResponse[QueryAllBalancesResponse]:
        """
        Query the balance associated with a particular address.
        """

        url = self.create_api_url(QUERY_PATHS["balances"].format(address=address))
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:
            return QueryResponse(
                data=QueryAllBalancesResponse.from_dict(resp.data),
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_delegator_delegations(
        self,
        address: str,
    ) -> QueryResponse[QueryDelegatorDelegationsResponse]:
        """
        Query the delegations associated with a delegator.
        """

        url = self.create_api_url(
            QUERY_PATHS["delegator_delegations"].format(delegator_address=address)
        )
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:

            delegator_delegations = QueryDelegatorDelegationsResponse.from_dict(
                resp.data,
            )
            return QueryResponse(
                data=delegator_delegations,
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_delegation_total_rewards(
        self, address: str
    ) -> QueryResponse[QueryDelegationTotalRewardsResponse]:
        """ """

        url = self.create_api_url(
            QUERY_PATHS["delegation_total_rewards"].format(delegator_address=address)
        )
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:

            delegation_total_rewards = QueryDelegationTotalRewardsResponse.from_dict(
                resp.data
            )
            return QueryResponse(
                data=delegation_total_rewards, status_code=resp.status_code
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def broadcast(self, tx) -> str:
        url = self.create_api_url(TX_PATHS["tx"])
        resp = requests.post(
            url=url,
            json=tx,
        )
        if resp.status_code == 200:
            return resp.json()
        raise Exception("error broadcasting")

    # ---------------------------------------------------------------------------------------------
    # RPC
    # ---------------------------------------------------------------------------------------------
    def _get_sync_info(self) -> QueryResponse[SyncInfo]:
        url = self.create_rpc_url(QUERY_PATHS["status"])
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:
            return QueryResponse(
                data=SyncInfo.from_dict(resp.data),
                status_code=resp.status_code,
            )

        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")
        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_height(self) -> QueryResponse[str]:
        """
        Query the height of the last block.
        """
        sync_info_resp = self._get_sync_info()

        if not sync_info_resp.data:
            raise Exception("Data returned by query is nil")

        try:
            return QueryResponse(
                data=sync_info_resp.data.latest_block_height,
                status_code=sync_info_resp.status_code,
            )
        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=sync_info_resp.status_code,
            )

    def get_last_hash(self) -> QueryResponse[str]:
        """
        Query the hash of the last block.
        """
        sync_info_resp = self._get_sync_info()

        if not sync_info_resp.data:
            raise Exception("Data returned by query is nil")

        try:
            return QueryResponse(
                data=sync_info_resp.data.latest_block_hash,
                status_code=sync_info_resp.status_code,
            )
        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=sync_info_resp.status_code,
            )

    def get_block_by_height(self, height: str) -> QueryResponse[ResultBlock]:
        """
        Query a block associated with a particular height.
        """
        url = self.create_rpc_url(QUERY_PATHS["block"].format(height=height))
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:
            block = Block.from_dict(resp.data["result"]["block"])
            block_id = BlockID.from_dict(resp.data["result"]["block_id"])

            return QueryResponse(
                data=ResultBlock(
                    block_id=block_id,
                    block=block,
                ),
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_block_by_hash(self, _hash: str) -> QueryResponse[ResultBlock]:
        """
        Query a block associated with a particular hash.
        """
        url = self.create_rpc_url(QUERY_PATHS["block_by_hash"].format(hash=_hash))
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:
            block = Block.from_dict(resp.data["result"]["block"])
            block_id = BlockID.from_dict(resp.data["result"]["block_id"])

            return QueryResponse(
                data=ResultBlock(
                    block_id=block_id,
                    block=block,
                ),
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )

    def get_tx_by_hash(self, _hash: str) -> QueryResponse[ResultTx]:
        """
        Query a transaction associated with a particular hash.
        """
        url = self.create_rpc_url(QUERY_PATHS["tx"].format(hash=_hash))
        resp = self._make_request(url)

        if not resp.is_success():
            return resp

        if not resp.data:
            raise Exception("Data returned by query is nil")

        try:
            return QueryResponse(
                data=ResultTx.from_dict(resp.data["result"]),
                status_code=resp.status_code,
            )

        except KeyError as e:
            return QueryResponse(
                error=f"Invalid response format: {str(e)}",
                status_code=resp.status_code,
            )
