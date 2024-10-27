from mantrapy.webhooks.hooks.webhook import Webhook
from mantrapy.webhooks.modules.utils import get_account_events


# Wrapper function to set address as a fixed parameter
def account_event_processor(address: str):
    return lambda events: get_account_events(address, events)


class AddressActivityWebhook(Webhook):

    def __init__(self, websocket_url, webhook_url, address):
        # Customize process function with the specific address
        process_fn = account_event_processor(address)
        # Initialize the base Webhook with the custom process function
        super().__init__(websocket_url, webhook_url, process_fn)
