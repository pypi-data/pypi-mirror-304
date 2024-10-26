from odyssey_exchange_api.requests.base import WebsocketRequest


class WebsocketKlineHistoryRequest(WebsocketRequest):
    symbol: str
    interval: str

    def build_request_data(self) -> dict:
        data = {
            "event": "req",
            "params": {
                "channel": f"market_{self.symbol}_kline_{self.interval}",
            }
        }
        return data
