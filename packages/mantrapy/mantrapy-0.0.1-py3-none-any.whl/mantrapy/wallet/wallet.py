import hashlib
from binascii import unhexlify
from hashlib import sha256

import bech32
import ecdsa

from mantrapy.wallet.hashing import ripemd160
from mantrapy.wallet.utils import new_hdwallet_from_mnemonic
from mantrapy.wallet.utils import new_mnemonic
from mantrapy.wallet.utils import privkey_to_pubkey


class Wallet:

    def __init__(self):
        self.mnemonic = ''
        self.privkey = ''
        self.address = ''

    def sign_document(self, doc: bytes) -> bytes:
        privkey = ecdsa.SigningKey.from_string(unhexlify(self.privkey), curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            doc, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize,
        )
        return signature_compact


def random_wallet() -> Wallet:
    return wallet_from_mnemonic(new_mnemonic())


def wallet_from_mnemonic(mnemonic: str) -> Wallet:
    w = Wallet()
    w.mnemonic = mnemonic
    generator = new_hdwallet_from_mnemonic(w.mnemonic)
    w.privkey = generator.private_key()
    compressed_public_key = privkey_to_pubkey(w.privkey)
    public_key_hash = ripemd160(sha256(compressed_public_key).digest())
    five_bit_r = bech32.convertbits(public_key_hash, 8, 5)
    if five_bit_r is not None:
        w.address = bech32.bech32_encode('mantra', five_bit_r)
    else:
        print('invalid address')
        raise Exception('failed to generate address')

    return w
