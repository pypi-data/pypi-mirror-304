import asyncio
import json
import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from mantrapy.server.databases import SessionLocal
from mantrapy.server.databases import Webhook
from mantrapy.server.event_processor import get_event_processor
from mantrapy.webhooks.chain_client import ChainClient

# Retrieve FastAPI's default logger
logger = logging.getLogger('uvicorn')


# data model for the request body
class WebhookRequest(BaseModel):
    url: str
    query: str


websocket_url = (
    'wss://rpc.dukong.mantrachain.io:443/websocket'
)
chain_client = ChainClient(websocket_url)

# In-memory cache for registered webhooks
registered_hooks_cache = {}


async def async_process_fn(process_fn, events, hook_id):
    """Wrapper to run process_fn with error handling."""
    try:
        process_fn(events)
    except Exception as e:
        logger.error(f'Error processing event in hook {hook_id}: {e}')


async def process_event(ws_event):
    # Decode the incoming message if it's JSON
    if isinstance(ws_event, str):
        ws_event = json.loads(ws_event)
    if 'events' in ws_event.get('result', {}) and 'message.msg_index' in ws_event[
        'result'
    ].get('events', {}):
        events = ws_event['result']['data']['value']['TxResult']['result']['events']

        # Create a list to hold all processing tasks
        tasks = []

        # Iterate through the cached hooks and create a task for each process_fn
        for hook_id, process_fn in registered_hooks_cache.items():
            tasks.append(
                asyncio.create_task(async_process_fn(process_fn, events, hook_id))
            )

        # Wait for all tasks to complete
        await asyncio.gather(*tasks)


async def process_events():
    """Listen for events from the ChainClient and post to registered webhooks."""
    async for ws_event in chain_client.subscribe("tm.event='Tx'"):
        logger.debug('Processing new events...')
        try:
            await process_event(ws_event)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f'Error parsing event data: {e}')
            logger.error('Raw event data:', ws_event)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await chain_client.connect()  # Connect to WebSocket
    with SessionLocal() as db:
        existing_hooks = db.query(Webhook).all()
        for hook in existing_hooks:
            try:
                # Attempt to create an event processor
                processor = get_event_processor(hook.id, hook.url, hook.query)
                # Cache the hooks and their corresponding event processor
                registered_hooks_cache[hook.id] = processor
            except ValueError as e:
                logger.error(
                    f'Error creating EventProcessor for hook ID {hook.id}: {e}',
                )
        logger.info(f'Found {len(existing_hooks)} hooks in the database.')

    task = asyncio.create_task(process_events())
    yield
    # Clean up and shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    try:
        # Close the WebSocket connection on server shutdow
        if chain_client.websocket:
            await chain_client.websocket.close()
    except Exception as e:
        logger.error(f'Error closing ws connection: {e}')


app = FastAPI(lifespan=lifespan)


@app.post('/webhooks/')
async def create_webhook(req: WebhookRequest):
    """Create a new webhook and persist it in the database."""
    # Generate a new unique hook ID (UUID)
    hook_id = str(uuid4())
    # Attempt to create an event processor
    try:
        processor = get_event_processor(hook_id, req.url, req.query)
    except ValueError as e:
        # Return a 400 error if get_event_processor fails
        raise HTTPException(status_code=400, detail=str(e))

    with SessionLocal() as db:
        new_webhook = Webhook(id=hook_id, query=req.query, url=req.url)
        db.add(new_webhook)
        db.commit()

    # Cache the new hook
    registered_hooks_cache[hook_id] = processor
    return {'message': 'Webhook created', 'hook_id': hook_id}


@app.delete('/webhooks/{hook_id}')
async def delete_webhook(hook_id: str):
    """Remove a webhook from the database."""
    with SessionLocal() as db:
        webhook = db.query(Webhook).filter(Webhook.id == hook_id).first()
        if not webhook:
            raise HTTPException(status_code=404, detail='Webhook not found')

        db.delete(webhook)
        db.commit()

    # Remove from cache
    registered_hooks_cache.pop(hook_id, None)
    return {'message': 'Webhook deleted', 'hook_id': hook_id}


@app.get('/webhooks/')
async def get_webhooks():
    """List webhooks."""
    with SessionLocal() as db:
        webhooks = db.query(Webhook).all()

    return {'hooks': webhooks}


@app.get('/webhooks/{hook_id}')
async def get_webhook(hook_id: str):
    """Get webhook by ID."""
    with SessionLocal() as db:
        webhook = db.query(Webhook).filter(Webhook.id == hook_id).first()
        if not webhook:
            raise HTTPException(status_code=404, detail='Webhook not found')

    return {'hook': webhook}
