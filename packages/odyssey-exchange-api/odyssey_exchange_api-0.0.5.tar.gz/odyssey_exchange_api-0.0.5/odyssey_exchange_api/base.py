import os

DEFAULT_SPOT_URL = "https://openapi.odyssey.trade"
DEFAULT_FUTURES_URL = "https://futuresopenapi.odyssey.trade"
DEFAULT_WEBSOCKET_URL = "wss://ws.odyssey.trade/kline-api/ws"

BASE_SPOT_URL = os.environ.get("ODYSSEY_EXCHANGE_SPOT_URL", DEFAULT_SPOT_URL)
BASE_FUTURES_URL = os.environ.get("ODYSSEY_EXCHANGE_FUTURES_URL", DEFAULT_FUTURES_URL)
BASE_WEBSOCKET_URL = os.environ.get("ODYSSEY_EXCHANGE_WEBSOCKET_URL", DEFAULT_WEBSOCKET_URL)
