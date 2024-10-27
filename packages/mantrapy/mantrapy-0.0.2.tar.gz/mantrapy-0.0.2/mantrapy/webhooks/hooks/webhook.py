import json

from mantrapy.webhooks.chain_client import ChainClient
from mantrapy.webhooks.event_processor import EventProcessor


# Generic Webhook class
class Webhook:

    def __init__(
        self, websocket_url, webhook_url, process_fn, event_query="tm.event='Tx'",
    ):
        self.client = ChainClient(websocket_url)
        self.processor = EventProcessor(webhook_url, process_fn)
        self.query = event_query

    async def listen(self):
        async for ws_event in self.client.subscribe(self.query):
            try:
                if isinstance(ws_event, str):
                    ws_event = json.loads(ws_event)
                if 'events' in ws_event.get(
                    'result',
                    {},
                ) and 'message.msg_index' in ws_event['result'].get(
                    'events',
                    {},
                ):
                    events = ws_event['result']['data']['value']['TxResult']['result'][
                        'events'
                    ]
                    self.processor.process_events(events)
            except (json.JSONDecodeError, KeyError) as e:
                print(f'Error parsing event data: {e}')
                print('Raw event data:', ws_event)
