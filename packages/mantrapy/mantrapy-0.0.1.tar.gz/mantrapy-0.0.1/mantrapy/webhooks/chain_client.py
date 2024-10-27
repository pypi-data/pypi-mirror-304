import asyncio

import websockets


class ChainClient:

    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        self.websocket = None

    async def connect(self):
        """Establish a connection to the WebSocket server."""
        if self.websocket is not None and self.websocket.open:
            return  # Already connected

        try:
            self.websocket = await websockets.connect(self.websocket_url)
            print('WebSocket connection established.')
        except (websockets.InvalidURI, websockets.InvalidHandshake) as e:
            print(f'Failed to connect: {e}')
            self.websocket = None

    async def subscribe(self, query, max_retries=3):
        """Subscribe to the specified query and yield messages."""
        if self.websocket is None or not self.websocket.open:
            await self.connect()
        retry_count = 0
        while retry_count < max_retries:
            try:
                await self.websocket.send(
                    f'{{"jsonrpc":"2.0","method":"subscribe","params":["{query}"],"id":1}}',
                )
                while True:
                    message = await self.websocket.recv()
                    yield message
            except websockets.ConnectionClosedError as e:
                print(f'Connection error: {e}. Retrying...')
                retry_count += 1
                await asyncio.sleep(2)  # Wait before retrying
            except websockets.InvalidStatusCode as e:
                print(f'Invalid status code error: {e}. Retrying...')
                retry_count += 1
                await asyncio.sleep(2)  # Wait before retrying
            except asyncio.TimeoutError:
                print('Connection timed out. Retrying...')
                retry_count += 1
                await asyncio.sleep(2)  # Wait before retrying

        print('Max reconnect attempts reached. Exiting...')
