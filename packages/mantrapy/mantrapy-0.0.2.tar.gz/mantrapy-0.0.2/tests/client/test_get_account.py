from mantrapy.client.client import Client
from mantrapy.constants.constants import Constants

TEST_MNEMONIC = "anger pencil awful note doctor like slide muffin hungry keen appear eight barrel stone quiz candy loud blush load three analyst buddy health member"  # noqa: E501
TEST_ADDRESS = "mantra1n4u9s9h3c670s7wsfycf6v7d7f2t55ql9gm3sj"
# TEST_PUBKEY = 'AhTyXF70ourZP+jEpSfzY5s9BF+sc0+5Oy2gawL1skKI'


def test_account_not_exists():
    account = "mantra1dgf0qzymxek2rpsy99hkcp647cnr4s7khsgcvs"
    constants = Constants()
    client = Client(constants.api_endpoint, constants.rpc_endpoint)
    resp = client.get_account(account)
    assert resp.status_code == 404


def test_account_with_no_pubkey():
    account = "mantra12vhp9wge82rcwhcts2fqq5ucczeekgmkjy2vz0"
    constants = Constants().testnet()
    client = Client(constants.api_endpoint, constants.rpc_endpoint)
    resp = client.get_account(account)
    assert resp.status_code == 200
    assert resp.data is not None
    assert resp.data.account.pub_key is None


def test_account_valid():
    account = "mantra1n4u9s9h3c670s7wsfycf6v7d7f2t55ql9gm3sj"
    constants = Constants()
    client = Client(constants.api_endpoint, constants.rpc_endpoint)
    resp = client.get_account(account)
    assert resp.status_code == 200
    assert resp.data is not None
    assert resp.data.account.pub_key is not None
