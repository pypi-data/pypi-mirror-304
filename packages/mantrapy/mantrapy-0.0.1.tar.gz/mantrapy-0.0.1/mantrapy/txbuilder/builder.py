import base64

import requests

from mantrapy.client.client import Client
from mantrapy.constants.constants import Constants
from mantrapy.txbuilder.messages import generate_bank_send_msg
from mantrapy.txbuilder.transaction import (
    create_sig_doc,
    create_tx_raw,
    create_tx_template,
)
from mantrapy.wallet.wallet import Wallet


class TxBuilder:

    def __init__(self, wallet: Wallet, is_testnet: bool = False) -> None:
        self.wallet = wallet
        self.constants = Constants()
        if is_testnet:
            self.constants.testnet()
        self.client = Client(self.constants.api_endpoint, self.constants.rpc_endpoint)
        self.update_account_info()

    def update_account_info(self):
        acc = self.client.get_account(self.wallet.address)
        self.pubkey = base64.b64decode(acc.data.account.pub_key.key)
        self.account_number = acc.data.account.account_number
        self.sequence = acc.data.account.sequence

    def sign_message(self, sign_doc) -> bytes:
        return self.wallet.sign_document(sign_doc)

    def prepare_tx(self, body, auth_info, signature) -> str:
        txraw = create_tx_raw(
            body.SerializeToString(), auth_info.SerializeToString(), signature
        )
        txbytes = txraw.SerializeToString()
        return base64.b64encode(txbytes).decode("utf-8")

    def broadcast_tx(self, body, auth_info, signature) -> str:
        tx_bytes = self.prepare_tx(body, auth_info, signature)
        tx_to_broadcast = {
            "tx_bytes": tx_bytes,
            "mode": "BROADCAST_MODE_SYNC",
        }

        self.client.broadcast(tx_to_broadcast)

    def broadcast_bytes(self, tx_bytes):
        tx_to_broadcast = {
            "tx_bytes": tx_bytes,
            "mode": "BROADCAST_MODE_SYNC",
        }

        resp = requests.post(
            url=self.constants.api_endpoint + "/cosmos/tx/v1beta1/txs",
            json=tx_to_broadcast,
        )
        if resp.status_code == 200:
            return resp.json()
        raise Exception("error broadcasting")

    # Messages
    def bank_send(self, dst: str, amount: int, denom: str) -> str:
        fee = "3257"
        gas = "271402"

        msg = generate_bank_send_msg(self.wallet.address, dst, str(amount), denom)

        body, auth_info = create_tx_template(
            msg, "", fee, self.constants.denom, gas, self.pubkey, int(self.sequence)
        )
        sign_doc = create_sig_doc(
            body, auth_info, self.constants.chain_id, int(self.account_number)
        )

        return body, auth_info, sign_doc
