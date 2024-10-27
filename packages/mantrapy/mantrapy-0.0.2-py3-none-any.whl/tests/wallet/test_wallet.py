from mantrapy.wallet.wallet import wallet_from_mnemonic

TEST_MNEMONIC = 'anger pencil awful note doctor like slide muffin hungry keen appear eight barrel stone quiz candy loud blush load three analyst buddy health member'  # noqa: E501
TEST_ADDRESS = 'mantra1qj5477l97xch25a7dfs6mjpcxp5n209purvvwg'
TEST_PUBKEY = 'AhTyXF70ourZP+jEpSfzY5s9BF+sc0+5Oy2gawL1skKI'


def test_wallet_generator():
    w = wallet_from_mnemonic(TEST_MNEMONIC)
    assert w.address == TEST_ADDRESS
    assert w.pubkey == TEST_PUBKEY
