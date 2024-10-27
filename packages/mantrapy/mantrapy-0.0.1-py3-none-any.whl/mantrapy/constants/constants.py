import os


class Constants:

    def __init__(self):
        self.api_endpoint = os.getenv(
            'API_ENDPOINT',
            'https://api.mantrachain.io',
        )
        self.rpc_endpoint = os.getenv(
            'API_ENDPOINT',
            'https://rpc.mantrachain.io',
        )
        self.chain_id = os.getenv('CHAIN_ID', 'mantra-1')
        self.denom = os.getenv('DENOM', 'uom')

    def testnet(self):
        self.api_endpoint = 'https://api.dukong.mantrachain.io/'
        self.rpc_endpoint = 'https://rpc.dukong.mantrachain.io/'
        self.denom = 'uom'
        self.chain_id = 'mantra-dukong-1'
