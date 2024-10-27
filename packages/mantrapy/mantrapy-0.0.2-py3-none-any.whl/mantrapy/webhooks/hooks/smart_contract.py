from mantrapy.webhooks.hooks.webhook import Webhook
from mantrapy.webhooks.modules.smart_contract import get_smart_contracts_events


class SmartContractWebhook(Webhook):

    def __init__(self, websocket_url, webhook_url):
        # Initialize the base Webhook with the custom process function
        super().__init__(
            websocket_url,
            webhook_url,
            get_smart_contracts_events,
        )
