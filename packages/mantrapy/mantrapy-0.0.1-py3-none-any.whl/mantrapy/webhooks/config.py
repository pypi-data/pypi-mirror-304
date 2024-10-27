from pydantic_settings import BaseSettings


class Config(BaseSettings):
    websocket_url: str = 'wss://rpc.hongbai.mantrachain.io:443/websocket'
    webhook_url: str = 'https://your-webhook-url'

    class Config:
        env_file = '.env'
