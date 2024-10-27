from mantrapy.webhooks.hooks.webhook import Webhook
from mantrapy.webhooks.modules.tokenfactory import get_token_factory_events


class TokenFactoryWebhook(Webhook):

    def __init__(self, websocket_url, webhook_url):
        # Initialize the base Webhook with the custom process function
        super().__init__(websocket_url, webhook_url, get_token_factory_events)
