from binascii import unhexlify

import ecdsa
import mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import ATOM as SYMBOL

PATH = "m/44'/118'/0'/0/0"


def new_mnemonic():
    return mnemonic.Mnemonic(language='english').generate(strength=256)


def privkey_to_pubkey(privkey: str) -> bytes:
    key = ecdsa.SigningKey.from_string(
        unhexlify(privkey),
        curve=ecdsa.SECP256k1,
    )
    pubkey_obj = key.get_verifying_key()
    return pubkey_obj.to_string('compressed')  # type: ignore


def new_hdwallet_from_mnemonic(phrase: str):
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
    hd_wallet = hdwallet.from_mnemonic(phrase, 'english')
    hd_wallet.from_path(PATH)
    return hd_wallet
